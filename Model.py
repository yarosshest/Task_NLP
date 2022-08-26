import wget
import zipfile
import gensim
import os.path
from Handlers.Prep import Prep
from math import inf

def trunc(text, length):
    text = text.split(" ")[:length]
    text = " ".join(text)
    return text


class Model(object):
    model_url = 'http://vectors.nlpl.eu/repository/20/220.zip'

    def __init__(self):
        model_file = self.model_url.split('/')[-1]
        if not os.path.exists(model_file):
            print("Downloading model...")
            self.download()
        self.model = gensim.models.KeyedVectors.load_word2vec_format('model.bin', binary=True)
        self.prep = Prep()
        self.welcome_text = [self.prep.tag("Добрый день"),
                             self.prep.tag("Здравствуйте")]
        self.introduce_text = [self.prep.tag("Меня зовут"),
                               self.prep.tag("Да это Максим"), ]
        self.goodbye_text = [self.prep.tag("До свидания"),
                             self.prep.tag("Всего хорошего до свидания"),
                             self.prep.tag("Всего хорошего")]
        self.name_context = ["александр_PROPN",
                             "виктория_PROPN",
                             "сергей_PROPN",
                             "никита_PROPN",
                             "максим_NOUN",
                             "валентина_PROPN"]

    def download(self):
        model_file = self.model_url.split('/')[-1]
        wget.download(self.model_url)
        with zipfile.ZipFile(model_file, 'r') as archive:
            archive.extract('model.bin')

    def getDistance(self, first, second):
        return self.model.wmdistance(first.split(" "), second.split(" "))

    def check_context(self, text, patterns, min_similarity=0.7):
        text = self.prep.tag(text)
        res = list(map(lambda x: self.getDistance(text, x), patterns))
        return min(res) < min_similarity

    def check_welcome(self, text):
        return self.check_context(text, self.welcome_text, 0.7)

    def check_introduce(self, text):
        return self.check_context(trunc(text, 5), self.introduce_text, 1.08)

    def check_goodbye(self, text):
        return self.check_context(text, self.goodbye_text, 0.5)

    def check_word(self, word, context, gate=0.55):
        if word != "":
            if word not in self.model.key_to_index and "_NOUN" in word:
                word = word[:word.index("_")]
                word += "_PROPN"
            if word in self.model.key_to_index:
                res = list(map(lambda x:  1 - self.model.similarity(word, x, ), context))
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
            name = prep_text[prep_text.index("компания_NOUN") + 1]
            if "_NOUN" in name:
                return text[prep_text.index(name)]
            else:
                return False
        else:
            return False


if __name__ == '__main__':
    model = Model()
    print(model.prep.tag("Меня зовут ангелина компания диджитал бизнес звоним вам по поводу продления лицензии а мы с серым у вас скоро срок заканчивается"))
    print(model.get_company("Меня зовут ангелина компания диджитал бизнес звоним вам по поводу продления лицензии а мы с серым у вас скоро срок заканчивается"))
