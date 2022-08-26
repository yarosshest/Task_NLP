import csv
from tqdm import tqdm
from Dialog import Dialog
from Message import Message
from Model import Model

if __name__ == '__main__':
    with open('test_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        header = True
        ids = {}
        dialogs = []
        model = Model()
        print("Loading data...")
        for row in tqdm(reader):
            start = row[0].split(',')
            if header:
                header = False
            else:
                if start[0] not in ids:
                    ids.update({start[0]: True})
                    dialog = Dialog(int(start[0]))
                    dialog.append(Message(int(start[1]), start[2], start[3:] + row[1:]))
                    dialogs.append(dialog)
                else:
                    dialogs[-1].append(Message(int(start[1]), start[2], start[3:] + row[1:]))
                text = start[3:] + row[1:]
                text = ' '.join(text)
                if model.check_goodbye(text):
                    print(text)

    pass