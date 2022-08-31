import wget
import zipfile
import gensim
import os.path
from Prep import Prep
from math import inf


def trunc_front(text, length):
    text = text.split(" ")[:length]
    text = " ".join(text)
    return text


def trunc_back(text, length):
    text = text.split(" ")[-length:]
    text = " ".join(text)
    return text


class Model(object):
    model_url = 'http://vectors.nlpl.eu/repository/20/220.zip'

    def __init__(self):
        model_file = self.model_url.split('/')[-1]
        if not os.path.exists(model_file):
            print("Downloading model...")
            self.download()
            print("Model downloaded")
        self.model = gensim.models.KeyedVectors.load_word2vec_format('model.bin', binary=True)
        self.prep = Prep()
        self.hellow_text = ["добрый_ADJ день_NOUN",
                            "здравствуйте_VERB"]
        self.introduce_text = ["меня_PRON зовут_VERB александр_PROPN",
                               "да_CCONJ это_PRON александр_PROPN"]
        self.goodbye_text = ["до_ADP свидания_NOUN".split(" "),
                             "всего_PRON хорошего_ADJ до_ADP свидания_NOUN".split(" "),
                             "до_ADP свидания_NOUN хорошего_ADJ вечера_ADV".split(" "),
                             "все_PRON хорошо_ADV".split(" "),
                             "всего_PRON доброго_ADV".split(" "),
                             "всего_PRON хорошего_ADJ".split(" ")]
        self.name_context = ["александр_PROPN",
                             "виктория_PROPN",
                             "сергей_PROPN",
                             "никита_PROPN",
                             "максим_NOUN",
                             "валентина_PROPN"]
        self.company_context = ["сбербанк_NOUN",
                                "торговый_ADJ дом_NOUN копейка_NOUN",
                                "российский_ADJ алюминий_NOUN",
                                "национальная_ADJ компьютерная_ADJ корпорация_NOUN", ]

    def download(self):
        model_file = self.model_url.split('/')[-1]
        wget.download(self.model_url)
        with zipfile.ZipFile(model_file, 'r') as archive:
            archive.extract('model.bin')

    def getDistance(self, first, second):
        return self.model.wmdistance(first.split(" "), second.split(" "))

    def check_distance(self, text, patterns):
        text = self.prep.tag(text)
        res = list(map(lambda x: self.getDistance(text, x), patterns))
        return min(res)

    def check_hellow(self, text):
        return self.check_distance(text, self.hellow_text) < 0.7

    def check_introduce(self, text):
        return self.check_distance(trunc_front(text, 4), self.introduce_text) < 1.5

    # в словаре моделлей нет слов прощания поэтому проверка будет по леммам
    def check_goodbye(self, text):
        text = trunc_back(text, 4)
        text = self.prep.tag(text).split(" ")
        res = []
        for i in self.goodbye_text:
            flag = True
            for j in i:
                if j not in text:
                    flag = False
            res.append(flag)
        return max(res)

    def check_company(self, text):
        return self.check_distance(text, self.company_context)

    def check_word(self, word, context, gate=0.55):
        if word != "":
            if word not in self.model.key_to_index and "_NOUN" in word:
                word = word[:word.index("_")]
                word += "_PROPN"
            if word in self.model.key_to_index:
                res = list(map(lambda x: 1 - self.model.similarity(word, x, ), context))
                res = list(map(lambda x: x if x < gate else inf, res))
                return min(res)
            else:
                return inf
        else:
            return inf

    def get_name(self, text):
        prep_text = self.prep.tag(text).split(" ")
        text = text.split(" ")
        res = list(map(lambda x: self.check_word(x, self.name_context), prep_text))
        res = dict(zip(text, res))
        for key, value in dict(res).items():
            if value == inf:
                del res[key]

        if res != {}:
            return min(res, key=res.get)
        else:
            return False

    def get_company(self, text):
        prep_text = self.prep.tag(text).split(" ")
        text = text.split(" ")
        if "компания_NOUN" in prep_text and prep_text.index("компания_NOUN") != len(prep_text) - 1:
            start = prep_text.index("компания_NOUN") + 1
            if "_NOUN" in prep_text[start]:
                name = text[start]
            else:
                name = False

            if len(prep_text) - 1 < start + 5:
                length = len(prep_text) - 1
            else:
                length = start + 5
            min = inf
            for i in range(start, length + 1):
                dist = self.check_company(" ".join(text[start:i + 1]))
                if dist < min:
                    min = dist
                    end = i

            if name and min > 1.3:
                return name
            elif min < 1.1:
                return " ".join(text[start:end + 1])
            else:
                return False
        else:
            return False


if __name__ == '__main__':
    model = Model()
    print(model.check_goodbye("Транспортная компания хорошо а у вас уже вот все интеграции сделаны ну то есть там каналы коммуникации от клиентов поступления ледов вот это вот уже сделано или это вы еще только планируете все настраивать"))
