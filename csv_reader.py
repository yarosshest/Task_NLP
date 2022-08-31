import csv
from Dialog import Dialog
from Message import Message
from Model import Model


def read_csv():
    with open('test_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        header = True
        ids = {}
        dialogs = []
        print("Loading data...")
        for row in reader:
            start = row[0].split(',')
            if header:
                header = False
            else:
                if start[0] not in ids:
                    ids.update({start[0]: True})
                    dialog = Dialog(int(start[0]))
                    dialog.append(Message(int(start[1]), start[2], " ".join(start[3:] + row[1:])))
                    dialogs.append(dialog)
                else:
                    dialogs[-1].append(Message(int(start[1]), start[2], " ".join(start[3:] + row[1:])))
    return dialogs


if __name__ == '__main__':
    read_csv()
    pass
