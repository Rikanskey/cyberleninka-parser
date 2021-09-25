from searcher import Searcher


class Controller:

    def __init__(self):
        self.__searcher = Searcher()

    def start(self, configuration):
        if configuration.filter_var:
            return self.__searcher.search_articles(configuration.keywords, configuration.max_page,
                                                   [configuration.filter_var])
        return self.__searcher.search_articles(configuration.keywords, configuration.max_page)
