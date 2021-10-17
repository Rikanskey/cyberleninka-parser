import re

import nltk
from nltk.corpus import stopwords
from yargy import *
from yargy.predicates import *

nltk.download('stopwords')


def __skip_special_characters(word):
    i = 0
    ch = word[i]
    while ch < 'A':
        i += 1
        ch = word[i]
    return word[i:]


def __search_keywords(filename):
    with open(filename, 'r') as file:
        text = file.read()
        i = re.search(r'Ключевые\s*слова:', text)
        if not i:
            return [], ''
        keywords_string = text[i.start():]
        keywords = keywords_string[len(i.group()):keywords_string.find('.')].split(',')
        keywords = [__skip_special_characters(word) for word in keywords]
        file.close()
        return keywords, text


def __create_rule(split_keyword):
    if len(split_keyword) == 1:
        return rule(gram('NOUN'), dictionary({split_keyword[0]}))
    elif len(split_keyword) == 2:
        return rule(gram('NOUN'), dictionary({split_keyword[0]}), dictionary({split_keyword[1]}))
    elif len(split_keyword) == 3:
        return rule(gram('NOUN'), dictionary({split_keyword[0]}), dictionary({split_keyword[1]}),
                    dictionary({split_keyword[2]}))
    else:
        return None


def __remove_stop_words(words, word_pack):
    return [word for word in words if word not in word_pack]


def __append_result(result_dict, keyword, words):
    for word in words:
        if word not in result_dict[keyword]:
            result_dict[keyword].append(word)


def __collect_map(keywords, text):
    word_pack = stopwords.words('russian')
    result_dict = {}
    for keyword in keywords:
        result_dict[keyword] = []
        kw = ' '.join(keyword.split()).split(' ')
        rw = __create_rule(kw)
        if rw:
            par = Parser(rw)
            for match in par.findall(text):
                found_words = [x.normalized for x in match.tokens if x.normalized not in kw]
                found_words_without_stops = __remove_stop_words(found_words, word_pack)
                __append_result(result_dict, keyword, found_words_without_stops)
    return result_dict


def collect_tags(filename):
    keywords, text = __search_keywords(filename)

    return __collect_map(keywords, text)


if __name__ == '__main__':
    res = collect_tags('text.txt')
    for key in res.keys():
        print(f'{key}: {res[key]}')
