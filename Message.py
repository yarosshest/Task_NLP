class Message:
    hellow = False
    goodbye = False
    name = False
    company = False

    def __init__(self, num, role, text):
        self.id = num
        self.role = role
        self.text = text

    def get_data(self):
        return [self.id, self.role, self.text, self.hellow, self.goodbye, self.name, self.company]

    def check(self, model):
        if model.check_hellow(self.text):
            self.hellow = True
        elif model.check_goodbye(self.text):
            self.goodbye = True

        if not self.hellow and model.check_introduce(self.text):
            self.name = model.get_name(self.text)

        company = model.get_company(self.text)
        if company:
            self.company = company
        return True
