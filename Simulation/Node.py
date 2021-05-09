
class Node:

    def __init__(self, id ,type):
        self.type = type
        self.id = id
        self.people_assigned = []

    def assign_people(self, people):
        self.people_asigned = people
