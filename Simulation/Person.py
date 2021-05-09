
class Person:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.init_agenda(type)
        self.infection = None
        self.phone = []

    def init_agenda(self, type):
        if type == 'student':
            self.agenda = ['H', 'S', 'R', 'H']
        elif type == 'worker':
            self.agenda = ['H', 'W', 'R', 'H']
        elif type == 'stay-at-home':
            self.agenda = ['H', 'H', 'H', 'H']
        elif type == 'elderly':
            self.agenda = ['H', 'R', 'H', 'H']