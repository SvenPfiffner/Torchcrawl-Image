import os
from .xml import XMLData, XMLAtom
import requests
from bs4 import BeautifulSoup
import shutil
import cv2

class Crawler:

    def __init__(self, working_dir, force_overwrite=False):
        """
        Initializes a Crawler object.

        Args:
            working_dir (str): The path to the working directory.
            force_overwrite (bool, optional): Whether to overwrite the working directory if it already exists. 
                Defaults to False.

        Raises:
            ValueError: If the working directory already exists and force_overwrite is set to False.
        """
        self.working_dir = working_dir
        self.data = XMLData()

        # Create the working directory if it does not exist
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)
            # Create a subfolder "imgs" in the newly created directory
            os.makedirs(f"{self.working_dir}/imgs")

        elif not force_overwrite:
            raise ValueError("Working directory already exists. Set force_overwrite=True to overwrite.")
        else:
            # Delete the working directory if it already exists
            shutil.rmtree(self.working_dir)
            # Create the working directory
            os.makedirs(self.working_dir)
            # Create a subfolder "imgs" in the newly created directory
            os.makedirs(f"{self.working_dir}/imgs")
        
    def crawl(self, urls):
        """
        Crawls the given URLs and downloads images from them.

        Args:
            urls (str or list): The URL(s) to crawl. Can be a single URL as a string or a list of URLs.

        Raises:
            ValueError: If the input is not a string or a list of strings.

        Returns:
            None
        """
        if isinstance(urls, str):
            paths = self.get_images(urls)
        elif isinstance(urls, list):
            paths = []
            for url in urls:
                paths.extend(self.get_images(url))
        else:
            raise ValueError("Invalid input. urls must be a string or a list of strings.")

        offset = self.data.size
        for i, path in enumerate(paths):
            try:
                # Download the image from the path
                response = requests.get(path, stream=True)
                # Get the file extension from the URL
                extension = path.split('.')[-1]
                # Save the image with the correct file extension
                with open(f"{self.working_dir}/imgs/{i + offset}.{extension}", 'wb') as file:
                    shutil.copyfileobj(response.raw, file)
                # Add the image as a resource to the XMLData object
                # Get the size of the downloaded image
                image = cv2.imread(f"{self.working_dir}/imgs/{i + offset}.{extension}")

                # Add the image to the XMLData object
                self.data.add_entry(XMLAtom(filename=f"{i + offset}.{extension}",
                                            dtype=extension,
                                            path=f"{self.working_dir}/imgs/",
                                            source=path,
                                            shape=image.shape))

            except Exception as e:
                # Ignore this iteration if an exception occurred
                print(e)

            # Save the XML data to a file
            self.data.save_to_xml(f"{self.working_dir}/data.xml")


    def get_images(self, url):
        """
        Retrieves the URLs of all images on a given webpage.

        Args:
            url (str): The URL of the webpage to crawl.

        Returns:
            list: A list of image URLs found on the webpage.
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        image_paths = []

        # Find all image tags in the HTML
        image_tags = soup.find_all('img')

        # Extract the source (src) attribute of each image tag
        for img in image_tags:
            image_paths.append(img['src'])

        # Transform protocol relative URLs into absolute URLs
        for i, path in enumerate(image_paths):
            if path.startswith('//'):
                image_paths[i] = 'http:' + path

        return image_paths