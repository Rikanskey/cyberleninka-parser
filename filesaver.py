import re

import requests
import shutil
import os
from pdfminer.high_level import extract_text

from scanedfileparser import parse_scan

PDF_NAME = 'temp.pdf'
TEXT_FILE_NAME = 'text.txt'


def __check_document(text_file_name, pdf_file_name):
    with open(text_file_name, 'r') as file:
        text = file.read()
        t = re.search(r'Ключевые\*слова', text)
        file.close()
        if not t:
            return parse_scan(pdf_file_name)
        else:
            return text_file_name


def get_document(article_link):
    try:
        article = requests.get(article_link + '/pdf', stream=True)
    except requests.HTTPError as e:
        print(e)
        return ''

    with open(PDF_NAME, 'wb') as f:
        article.raw.decode_content = True
        shutil.copyfileobj(article.raw, f)

    with open(PDF_NAME, 'rb') as f:
        text = extract_text(f)
        with open(TEXT_FILE_NAME, 'w') as file:
            file.write(text)
            file.close()

        f.close()
        text_file_name = __check_document(file.name, f.name)
        os.remove(PDF_NAME)
        return text_file_name


if __name__ == '__main__':
    get_document('https://cyberleninka.ru/article/n/sozdanie-mnogozvennogo-programmnogo-kompleksa-'
                 'dlya-interaktivnogo-obucheniya')
