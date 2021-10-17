from filesaver import get_document, TEXT_FILE_NAME
from tagcollector import collect_tags
import os


class MindMapCreator:

    def __remove_files(self):
        os.remove(TEXT_FILE_NAME)

    def create_mind_map(self, article_link):
        text_document_name = get_document(article_link)
        tags = collect_tags(text_document_name)
        self.__remove_files()
        return tags


if __name__ == '__main__':
    cr = MindMapCreator()
    cr.create_mind_map('https://cyberleninka.ru/article/n/vypolnenie-javascript-kompozitsiy-wps'
                       '-servisov-v-raspredelennoy-geterogennoy-srede')
