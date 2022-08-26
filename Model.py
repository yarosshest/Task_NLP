import wget
import zipfile
import gensim
import os.path
from Handlers.Prep import PrepText


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
        else:
            self.model = gensim.models.KeyedVectors.load_word2vec_format('model.bin', binary=True)
        self.prep = PrepText()
        self.welcome_text = [self.prep.tag_ud("Добрый день"),
                             self.prep.tag_ud("Здравствуйте")]
        self.introduce_text = [self.prep.tag_ud("Меня зовут"),
                               self.prep.tag_ud("Да это Максим"),]
        self.goodbye_text = [self.prep.tag_ud("До свидания"),
                             self.prep.tag_ud("Всего хорошего до свидания"),
                             self.prep.tag_ud("Всего хорошего")]

    def download(self):
        model_file = self.model_url.split('/')[-1]
        wget.download(self.model_url)
        with zipfile.ZipFile(model_file, 'r') as archive:
            archive.extract('model.bin')

    def getDistance(self, first, second):
        return self.model.wmdistance(first.split(" "), second.split(" "))

    def check_context(self, text, patterns, min_similarity=0.7):
        text = self.prep.tag_ud(text)
        res = list(map(lambda x: self.getDistance(text, x), patterns))
        return min(res) < min_similarity

    def check_welcome(self, text):
        return self.check_context(text, self.welcome_text, 0.7)

    def check_introduce(self, text):
        return self.check_context(trunc(text, 5), self.introduce_text, 1.08)

    def check_goodbye(self, text):
        return self.check_context(text, self.goodbye_text, 0.5)


if __name__ == '__main__':
    model = Model()
    p = [1, 2, 3, ][:5]
    print(model.check_introduce(
        "Да это анастасия"))
