
class Person:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.init_agenda(type)
        self.infection = None
        self.phone = []
        self.workplace = None
        self.home = None
        self.school = None

    def init_agenda(self, type):
        if type == 'student':
            self.agenda = ['H', 'S', 'R', 'H']
        elif type == 'worker':
            self.agenda = ['H', 'W', 'R', 'H']
        elif type == 'stay-at-home':
            self.agenda = ['H', 'H', 'H', 'H']
        elif type == 'elderly':
            self.agenda = ['H', 'R', 'H', 'H']

    def set_workplace(self, workplace):
        self.workplace = workplace

    def set_home(self, home):
        self.home = home

    def set_school(self, school):
        self.school = school
