from abc import ABC, abstractmethod

class Source(ABC):

    def __init__(self, **kwargs):
        assert kwargs.get('name', None), "Debe definir un name"
        assert kwargs.get('logo', None), "Debe definir un logo"

        self.name = kwargs.get('name')
        self.logo = kwargs.get('logo')
        self.header_color = kwargs.get('header_color', 'black')
        self.header_background = kwargs.get('header_background', '#2f2f2f')

    @abstractmethod
    def do_search(self, search_word):
        pass

    @abstractmethod
    def get_search_results(self, serie_id, columns=None, rename_column=None):
        pass

    @abstractmethod
    def get_data_serie(self, id):
        pass