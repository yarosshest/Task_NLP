class Message:
    hellow = False
    goodbye = False
    name = None
    company = None

    def __init__(self, num, role, text):
        self.id = num
        self.role = role
        self.text = text

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
