from abc import abstractmethod, ABC


class Transformation(ABC):

    def __init__(self, **kwargs):
        assert kwargs.get('name', None), "Se debe definir un nombre."
        assert kwargs.get('suffix', None), "Se debe definir un sufijo"

        self.name = kwargs.get('name')
        self.suffix = "_{}".format(kwargs.get('suffix'))
        self.units_show = kwargs.get('units_show', None)

    @abstractmethod
    def transform(self):
        pass