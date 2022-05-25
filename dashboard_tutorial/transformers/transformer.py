from abc import abstractmethod, ABC


class Transformation(ABC):
    """
    A class used to represent a Trasnformation Type

    ...

    Attributes
    ----------
    name : str
        the name of the transform to show
    suffix : str
        suffix of the transform to show
    units_show : str
        units to show when transform is applied

    Methods
    -------
    transform(search_word)
        Do the transformation
    """
    def __init__(self, **kwargs):
        assert kwargs.get('name', None), "Must define a name."
        assert kwargs.get('suffix', None), "Must define a suffix."

        self.name = kwargs.get('name')
        self.suffix = "_{}".format(kwargs.get('suffix'))
        self.units_show = kwargs.get('units_show', None)

    @abstractmethod
    def transform(self):
        pass