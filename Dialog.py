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
