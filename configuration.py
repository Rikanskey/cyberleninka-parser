class CyberleninkaConfiguration:

    RSCI_VAR = 22
    VAK_VAR = 8
    SCOPUS_VAR = 2

    def __init__(self, max_page=3, keywords=''):
        self.__max_page = max_page
        self.__filter_var = 0
        self.__keywords = keywords

    @property
    def max_page(self):
        return self.__max_page

    @max_page.setter
    def max_page(self, value):
        self.__max_page = value

    @property
    def filter_var(self):
        return self.__filter_var

    @filter_var.setter
    def filter_var(self, value):
        self.__filter_var = value

    @property
    def keywords(self):
        return self.__keywords

    @keywords.setter
    def keywords(self, value):
        self.__keywords = value

