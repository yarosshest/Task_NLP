class Dialog:
    def __init__(self, num):
        self.id = num
        self.client_mes = []
        self.man_mes = []

    def append(self, message):
        if message.role == "client":
            self.client_mes.append(message)
        elif message.role == "manager":
            self.man_mes.append(message)

    def check_HG(self):
        h = False
        g = False
        for i in self.man_mes:
            if i.hellow:
                h = True
            elif i.goodbye:
                g = True
        return h and g

    def get_name_man(self):
        for i in self.man_mes:
            if i.name:
                return i.name
        return False

    def get_hellow(self):
        for i in self.man_mes:
            if i.hellow:
                return i.text
        return False

    def get_text_name_man(self):
        for i in self.man_mes:
            if i.name:
                return i.text
        return False

    def get_goodbye(self):
        for i in self.man_mes:
            if i.goodbye:
                return i.text
        return False

    def get_company(self):
        for i in self.man_mes:
            if i.company:
                return i.company
        return False

    def check_dialogs(self, model):
        for i in self.man_mes:
            i.check(model)
        return True
