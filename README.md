**Important: This code is in the "proof-of-concept" state an not yet thoroughly tested or improved for efficiency** 

# Torchcrawl Image
The Torchcrawl Image package is a Python library that provides tools for web crawling and image analysis. It allows you to crawl web pages and extract images from them, storing them in a specified directory along with metadata. The package also provides functionality to analyze the metadata and load the images as a pytorch dataset for machine learning tasks.

This package is useful for tasks such as building image datasets for training machine learning models, web scraping for image data, and automating the labeling process for images. It simplifies the process of collecting and organizing image data from the web, making it easier to work with and analyze large amounts of image data.

## Requirements
```
requests
bs4
cv2
numpy
pytorch
```
```
tested with: python 3.12.2
```

## Quickstart

Create a new crawler and pass it a working directory. This will be the directory your dataset resides in. For security reasons the crawler will not write to or alter non-empty working directories. This behaviour can be changed via the ```force_overwrite``` flag.
```python
import torchcrawl_image 

crawler = torchcrawl_image.Crawler('./data', force_overwrite=True)
```
The crawl method of a crawler can be used to scan the web for images. It can either be passed a single url as a ```str``` or a collection of urls as a ```list[str]```. Calling the crawl method on a (collection of) urls reads their html code and looks for ```<img>``` tags to find images present on the sites.

```python
# Crawl a single source
crawler.crawl('https://en.wikipedia.org/wiki/Bee')
 # Crawl multiple sources
crawler.crawl(['https://en.wikipedia.org/wiki/Bee',
               'https://en.wikipedia.org/wiki/Lion',
               ...])
```
The found images are enumerated and stored in the crawlers working directory along with a ```data.xml``` file that keeps track of their source, shape, dtype etc.

To analyze the ```data.xml``` data, the ```XMLData``` object can be used. It serves as a custom collection of distinct image data entries in the xml, which in turn are wrapped by ```XMLAtom```.

```python
class XMLAtom:
    """
    Represents an XML atom object.

    Attributes:
        filename (str): The filename of the atom.
        path (str): The path of the atom.
        source (str): The source of the atom.
        shape (tuple): The shape of the atom.
        type (str): The type of the atom.
        label (str): The label of the atom

    Methods:
        __str__(): Returns a string representation of the XML atom.
    """
```

```python
# Read a data.xml into a XMLData object
data = XMLData()
data.load_from_xml("<dir>/data.xml")

# Iterate over data entries
for e in data:
    print(e.label)
    print(e.shape)
    ...

# Filter for specific entries
data_of_source = data.filter_by_source('https://en.wikipedia.org/wiki/Bee')
data_of_type = data.filter_by_type("jpg")
data_filtered = data.filter_entries(lambda x: x.label > 5)
```

To load the working directory with the images and metadata as a dataset, a ```TorchcrawlDataset``` object can be created by passing the working directory.

```TorchCrawlDataset``` implements a ```torch.utils.data.Dataset``` and can directly be used as a pytorch dataset. It implements ```__getitem__``` to pass the images in the working directory along with the corresponding labels stored in ```data.xml``` metadata.  

```python
data = torchcrawl_image.TorchcrawlDataset('./data')
```
Note that the crawler does **NOT** label the images in any way and thus each image will be labeled as ```"undefined"```.

To automate labeling, ```TorchcrawlDataset``` objects implement a ```label_data``` function.

```python
def label_function(img: np.ndarray):
    return np.mean(img)

def filter_function(atom: XMLAtom):
    return atom.dtype == "jpg"

# Label all images
data.label_data(label_function)

# Only label jpg images
data.label_data(label_function, filter_function)

# Get all labels present in the dataset
data.get_labels()
```
