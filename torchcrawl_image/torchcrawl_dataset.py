from .xml import XMLData, XMLAtom
import cv2
from torch.utils.data import Dataset
import os

class TorchcrawlDataset(Dataset):

    def __init__(self, working_dir):
        self.working_dir = working_dir
        data = XMLData()
        data.load_from_xml(f"{working_dir}/data.xml")
        self.data = data

    def get_data(self):
        """
        Returns the data in the dataset.

        Returns:
            list: A list of XMLAtom objects representing the data in the dataset.
        """
        return list(self.data.data.values())

    def get_images(self):
        """
        Returns a list of images in the dataset.

        Returns:
            list: A list of images in the dataset.
        """
        return [cv2.imread(f"{self.working_dir}/imgs/{d.filename}") for d in self.data]

    def get_labels(self):
        """
        Returns a list of labels in the dataset.

        Returns:
            list: A list of labels in the dataset.
        """
        return list(set([d.label for d in self.data]))

    def refresh(self):
        """
        Refreshes the dataset by removing images no longer present in the working directory
        from both the dataset and the XML file.
        """
        for d in self.data:
            if not os.path.exists(f"{self.working_dir}/imgs/{d.filename}"):
                self.data.remove_entry(d)
        self.data.save_to_xml(f"{self.working_dir}/data.xml")

    def label_data(self, label_function, filter=None):
        """
        Labels the data using the given label function.

        Args:
            label_function (function): The function to use for labeling the data.
            filter (function, optional): A function to filter the data before labeling. Defaults to None.

        """

        if filter is not None:
            labeled_data = self.data.filter_entries(filter)
        else:
            labeled_data = self.data

        for d in labeled_data:
            img = cv2.imread(f"{self.working_dir}/imgs/{d.filename}")
            d.label = label_function(img)

        # Rewrite the xml file after labeling
        self.data.save_to_xml(f"{self.working_dir}/data.xml")

    def __len__(self):
        """
        Returns the length of the dataset.

        Returns:
            int: The length of the dataset.
        """
        return len(self.data)
    
    def __getitem__(self, idx):
        """
        Get the item at the specified index.

        Parameters:
            idx (int): The index of the item to retrieve.

        Returns:
            tuple: A tuple containing the image and its corresponding label.
        """
        d = list(self.data.data.values())[idx] # TODO: Make this more efficient
        img = cv2.imread(f"{self.working_dir}/imgs/{d.filename}")
        return img, d.label
