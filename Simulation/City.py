from simulation.Type import Type


class City:

    def __init__(self):
        self.list_workplaces = []
        self.list_homes = []
        self.list_schools = []
        self.list_others = []

    def add_node(self, type_a, node):
        if type_a == Type.HOME:
            self.list_homes.append(node)
        elif type_a == Type.SCHOOL:
            self.list_schools.append(node)
        elif type_a == Type.WORKPLACE:
            self.list_workplaces.append(node)
        else:
            self.list_others.append(node)
