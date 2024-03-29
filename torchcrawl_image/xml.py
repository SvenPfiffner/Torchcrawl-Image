class XMLData:
    """
    Represents a collection of XML data entries.

    Attributes:
        data (dict): A dictionary to store the XML data entries.

    Methods:
        add_entry(atom): Adds an XMLAtom entry to the XMLData.
        remove_entry(atom): Removes an XMLAtom entry from the XMLData.
        filter_by_shape(shape): Filters the XMLData entries by shape.
        filter_by_source(source): Filters the XMLData entries by source.
        filter_by_type(dtype): Filters the XMLData entries by type.
        filter_entries(filter_func): Filters the XMLData entries based on a filter function.
        save_to_xml(path): Saves the XMLData to an XML file.
        load_from_xml(path): Loads XMLData from an XML file.
        __str__(): Returns a string representation of the XMLData.
    """

    def __init__(self, data={}):
        """
        Initializes an instance of the XMLData class.
        """
        self.data = data
        self.size = len(data)

    def add_entry(self, atom):
        """
        Adds an XMLAtom entry to the XMLData.

        Args:
            atom (XMLAtom): The XMLAtom object to add.

        """
        self.data[atom.filename] = atom
        self.size += 1

    def remove_entry(self, atom):
        """
        Removes an XMLAtom entry from the XMLData.

        Args:
            atom (XMLAtom): The XMLAtom object to remove.

        """
        del self.data[atom.filename]
        self.size -= 1

    def filter_by_shape(self, shape):
        """
        Filters the XMLData entries by shape.

        Args:
            shape (tuple): The shape to filter by.

        Returns:
            XMLData: A new XMLData object containing the filtered entries.

        """
        return self.filter_entries(lambda x: x.shape == shape)

    def filter_by_source(self, source):
        """
        Filters the XMLData entries by source.

        Args:
            source (str): The source to filter by.

        Returns:
            XMLData: A new XMLData object containing the filtered entries.

        """
        return self.filter_entries(lambda x: x.source == source)

    def filter_by_type(self, dtype):
        """
        Filters the XMLData entries by type.

        Args:
            dtype (str): The type to filter by.

        Returns:
            XMLData: A new XMLData object containing the filtered entries.

        """
        return self.filter_entries(lambda x: x.dtype == dtype)

    def filter_entries(self, filter_func):
        """
        Filters the XMLData entries based on a filter function.

        Args:
            filter_func (function): The filter function to apply.

        Returns:
            XMLData: A new XMLData object containing the filtered entries.

        """
        return XMLData({k: v for k, v in self.data.items() if filter_func(v)})

    def save_to_xml(self, path):
        """
        Saves the XMLData to an XML file.

        Args:
            path (str): The path to the XML file.

        """
        with open(path, "w") as f:
            f.write(str(self))

    def load_from_xml(self, path):
        """
        Loads XMLData from an XML file.

        Args:
            path (str): The path to the XML file.

        """
        with open(path, "r") as f:
            data = f.read()
            self.data = {}
            for entry in data.split("<img>")[1:]:
                filename = entry.split("<filename>")[1].split("</filename>")[0]
                dtype = entry.split("<type>")[1].split("</type>")[0]
                path = entry.split("<path>")[1].split("</path>")[0]
                source = entry.split("<source>")[1].split("</source>")[0]
                shape = (int(entry.split("<width>")[1].split("</width>")[0]),
                         int(entry.split("<height>")[1].split("</height>")[0]),
                         int(entry.split("<depth>")[1].split("</depth>")[0]))
                label = entry.split("<label>")[1].split("</label>")[0]
                self.add_entry(XMLAtom(filename, path, source, shape, dtype, label))

    def __str__(self):
        """
        Returns a string representation of the XMLData.

        Returns:
            str: The string representation of the XMLData.

        """
        return "".join(["<img>" + str(atom) + "</img>" for atom in self.data.values()])

    def __iter__(self):
        """
        Returns an iterator over the XMLData entries.

        Returns:
            iter: An iterator over the XMLData entries.
        """
        return iter(self.data.values())
    
class XMLAtom:
    """
    Represents an XML atom object.

    Attributes:
        filename (str): The filename of the atom.
        type (str): The type of the atom.
        path (str): The path of the atom.
        source (str): The source of the atom.
        shape (tuple): The shape of the atom.

    Methods:
        __str__(): Returns a string representation of the XML atom.
    """

    def __init__(self, filename, path, source, shape, dtype="unknown", label="undefined"):
        self.filename = filename
        self.path = path
        self.source = source
        self.shape = shape
        self.dtype = dtype
        self.label = label

    def __str__(self):
        return f"<filename>{self.filename}</filename>" \
            f"<type>{self.dtype}</type>" \
            f"<path>{self.path}</path>" \
            f"<source>{self.source}</source>" \
            f"<size><width>{self.shape[1]}</width>" \
            f"<height>{self.shape[0]}</height>" \
            f"<depth>{self.shape[2]}</depth></size>" \
            f"<label>{self.label}</label>"