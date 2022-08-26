import os
import corpy.udpipe as crp
import wget
from pathlib import Path


class Prep(object):
    model_url = r'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3131/russian-syntagrus-ud-2.5-191206.udpipe'
    model_file = Path(Path(__file__).parent, model_url.split('/')[-1])

    def __init__(self):

        if not os.path.exists(self.model_file):
            print('\nLoading the model teging')
            self.download()
        self.model = crp.Model(str(self.model_file))

    def download(self):
        wget.download(self.model_url)

    def tag(self, lem_text):
        lem_text = lem_text.split(' ')
        text = [list(self.model.process(w)) for w in lem_text]
        tagged_words = [s[0].words[1].form + '_' + s[0].words[1].upostag for s in text if s]

        return " ".join(tagged_words)


if __name__ == "__main__":
    prep = Prep()
    print(prep.tag("Добрый меня максим зовут компания китобизнес удобно говорить"))