import json

import bs4
import requests

from article import Article

TERM_LINK = '"link":'

API = 'https://cyberleninka.ru/api/search'
URL = 'https://cyberleninka.ru'

REQUEST_BODY = {
    'mode': 'articles',
    'size': 10,
}

ARTICLES_PER_PAGE = 10


class Searcher:

    def __try_parse_article(self, link, article):
        response_page = requests.get(link)
        bs_page = bs4.BeautifulSoup(response_page.text, 'html.parser')
        article.title = bs_page.i.text

        authors = bs_page.find('h2', {'class': 'right-title'}).span.text
        article.authors = authors[authors.find('—') + 2:]

        labels = bs_page.find('div', {'class': 'labels'})
        article.year = int(labels.time.text)

        rsci = bs_page.find('div', {'class': 'label rsci'})
        if rsci:
            article.rsci = True

        vak = bs_page.find('div', {'class': 'label vak'})
        if vak:
            article.vak = True

        scopus = bs_page.find('div', {'class': 'label scopus'})
        if scopus:
            article.scopus = True

    def parse_article_page(self, link):
        article = Article(link=link)

        try:
            self.__try_parse_article(link, article)

        except requests.HTTPError or AttributeError as e:
            print(e)

        return article

    def __try_parse_request(self, body, filters, results):
        response_json = requests.post(API, data=json.dumps(body)).text

        for article_num in range(ARTICLES_PER_PAGE):
            response_json = response_json[response_json.find(TERM_LINK) + len(TERM_LINK) + 1:]
            article_link = response_json[:response_json.find('"')]
            article = self.parse_article_page(URL + article_link)
            if filters is None or article.check_filter(filters[0]):
                results.append(article)
            response_json = response_json[response_json.find('}'):]

    def search_articles(self, keywords, max_page, filters=None):
        results = []
        body = REQUEST_BODY | {'q': keywords}

        if filters:
            body = body | {'catalogs': filters}

        for page in range(max_page):

            body = body | {'from': ARTICLES_PER_PAGE * page}

            try:
                self.__try_parse_request(body, filters, results)

            except requests.HTTPError as e:
                print(e)
                return []

        return results


if __name__ == '__main__':
    keywords = input('Input your keywords.\n').lower()
    pr = Searcher()
    res = pr.search_articles(keywords, 3)
    print(res)
