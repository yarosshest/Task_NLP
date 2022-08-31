from csv_reader import read_csv
from csv_get import get_csv
from Model import Model

if __name__ == '__main__':
    dialogs = read_csv()
    model = Model()

    for i in range(len(dialogs)):
        dialogs[i].check_dialogs(model)
        print(f"Диалог № {str(i)}")
        print(f"Менеджер поздоровался: {dialogs[i].get_hellow()}")
        print(f"Менеджер представил себя : {dialogs[i].get_text_name_man()}")
        print(f"Имя менеджера: {dialogs[i].get_name_man()}")
        print(f"Название компании: {dialogs[i].get_company()}")
        print(f"Менеджер попрощался: {dialogs[i].get_goodbye()}")
        print(f"Менеджер поздоровался и попрощался: {dialogs[i].check_HG()}")
    get_csv(dialogs)
