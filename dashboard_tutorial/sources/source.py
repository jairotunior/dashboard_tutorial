from abc import ABC, abstractmethod

class Source(ABC):
    """
    A class used to represent an Source Connection

    ...

    Attributes
    ----------
    name : str
        the name of the animal
    logo : str
        the uri of logo image
    header_color : str
        hex header color of the box in the search modal
    header_background : str
        hex background color of the box in the search modal

    Methods
    -------
    do_search(search_word)
        Do the search in the data source
    get_search_results(serie_id, columns=None, rename_column=None):
        Get the result of the search
    get_data_serie(id)
        Get data serie by id
    """
    def __init__(self, **kwargs):
        assert kwargs.get('name', None), "Must define a name"
        assert kwargs.get('logo', None), "Must define a logo"

        self.name = kwargs.get('name')
        self.logo = kwargs.get('logo')
        self.header_color = kwargs.get('header_color', 'black')
        self.header_background = kwargs.get('header_background', '#2f2f2f')

    @abstractmethod
    def do_search(self, search_word):
        """Do the time serie with the search_word

        Parameters
        ----------
        search_word : str
            The file location of the spreadsheet

        Returns
        -------
            None
        """
        pass

    @abstractmethod
    def get_search_results(self):
        """Return search results

        Parameters
        ----------

        Returns
        -------
            list
                a list with search results
        """
        pass

    @abstractmethod
    def get_data_serie(self, serie_id, rename_column=None):
        """Gets the data serie

        Parameters
        ----------
        serie_id : str
            The id of the serie in the data source
        rename_column : str, optional
            New name of the column of the time serie

        Returns
        -------
            Dataframe
                a pandas Dataframe with two columns: data and time serie value
        """
        pass