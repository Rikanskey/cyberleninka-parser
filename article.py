class Article:

    def __init__(self, title='', link='', authors=''):
        self.__title = title
        self.__link = link
        self.__authors = authors
        self.__year = 0
        self.__rsci = False
        self.__vak = False
        self.__scopus = False

    def check_filter(self, filter):
        if filter == 22 and not self.__rsci or filter == 8 and not self.__vak or filter == 2 and not self.__scopus:
            return False
        return True

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def link(self):
        return self.__link

    @link.setter
    def link(self, value):
        self.__link = value

    @property
    def authors(self):
        return self.__authors

    @authors.setter
    def authors(self, value):
        self.__authors = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value

    @property
    def rsci(self):
        return self.__rsci

    @rsci.setter
    def rsci(self, value):
        self.__rsci = value

    @property
    def vak(self):
        return self.__vak

    @vak.setter
    def vak(self, value):
        self.__vak = value

    @property
    def scopus(self):
        return self.__scopus

    @scopus.setter
    def scopus(self, value):
        self.__scopus = value



