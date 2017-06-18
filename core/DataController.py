"""
DataController

:Authors:
    Berend Klein Haneveld
"""


class DataController(object):
    """
    DataController is the base interface for
    the reader and writer.
    """
    def __init__(self):
        super(DataController, self).__init__()

        self.supportedExtensions = []

    def is_extension_supported(self, extension):
        """
        :type extension: basestring
        :rtype: bool
        """
        result = False

        for ext in self.supportedExtensions:
            if ext == extension:
                result = True
                break

        return result

    def get_supported_extensions_as_string(self):
        """
        Create string representation of all the supported file extensions.
        It will be formatted as follows: '*.mbr *.dcm'
        :rtype: basestr
        """
        stringRepresentation = ""
        for extension in self.supportedExtensions:
            stringRepresentation += ("*." + extension + " ")
        return stringRepresentation
