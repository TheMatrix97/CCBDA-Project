import random
import Person
from simulation.City import City
from simulation.Node import Node
from simulation.Type import Type
import numpy as np


class Simulation:
    def __init__(self, individuals, incubation, symptomatic, immunity, mortality, beacons, size_factor_city):
        self.elderly = []
        self.workers = []
        self.students = []
        self.population = self.generate_population(individuals)
        self.incubation = incubation
        self.symptomatic = symptomatic
        self.immunity = immunity
        self.mortality = mortality
        self.city = City(size_factor_city)
        self.generate_nodes()
        self.round = 0
        self.matrix_distance = None

    def generate_nodes(self): #Our population is assigned
        # Workplaces
        count = self.create_assign_nodes(Type.WORKPLACE, self.workers, 20, 40, 0)

        # Homes
        count = self.create_assign_nodes(Type.HOME, self.population, 1, 5, count)

        # School
        count = self.create_assign_nodes(Type.SCHOOL, self.students, 100, 200, count)

        # Others
        self.create_assign_nodes(Type.OTHER, self.population, 50, 100, count)

    def generate_distance_matrix(self):
        nodesx = self.city.get_nodes()
        nodesy = self.city.others
        self.matrix_distance = np.zeros((len(nodesx), len(nodesy)))
        i = 0
        j = 0
        for nodex in nodesx:
            for nodey in nodesy:
                #CalcDistance
                aux2 = nodesy[nodey]
                aux1 = nodesx[nodex]
                distance = self.calc_distance(aux1, aux2)
                self.matrix_distance[i][j] = distance
                j += 1
            i += 1
            j = 0
    @staticmethod
    def calc_distance(node1, node2):
        return pow(pow((node1.x - node2.x), 2) + pow((node1.y - node2.y), 2), 0.5)


    def start_simulation(self):
        #Gen distance matrix
        self.generate_distance_matrix()
        # Move everyone to home
        for person in self.population:
            if person.home is not None:
                self.city.homes[person.home].add_person(person)
            else:
                print(person.id)
        self.round = 1

    def advance_round(self):
        nodes = self.city.get_nodes()
        for node_aux in nodes:
            node = nodes[node_aux]
            for person in node.people_in_this_node:
                move = self.round % 4
                node.people_in_this_node.remove(person)
                if person.agenda[move] == 'H':
                    self.city.homes[person.home].add_person(person)
                elif person.agenda[move] == 'W':
                    self.city.workplaces[person.workplace].add_person(person)
                elif person.agenda[move] == 'S':
                    self.city.schools[person.school].add_person(person)
                elif person.agenda[move] == 'R':
                    id_loc = node.id
                    aux = list(self.city.get_nodes().keys()).index(id_loc)
                    on_puc_anar_rec = self.matrix_distance[aux]
                    on_puc_anar_index = np.argsort(on_puc_anar_rec)
                    #Choose random 10
                    n = random.randint(0, 9)
                    key = list(self.city.others.keys())[on_puc_anar_index[n]]
                    node_dest = self.city.others[key]
                    node_dest.add_person(person)
        self.round += 1


    def create_assign_nodes(self, type_a, people, max_num, min_num, count):
        determine_num = random.randint(int(len(people) / min_num), int(len(people) / max_num))
        nodes = []
        for i in range(count, determine_num + count):
            node = Node(i, type_a)
            nodes.append(node)
        # Assigned people workplaces
        capacity = len(people) / len(nodes)
        count_people = 0
        for node in nodes:
            people_assignment = 0
            is_empty = True
            while people_assignment < int(capacity+1) and count_people < len(people):
                if is_empty:
                    is_empty = False
                if type_a == Type.WORKPLACE:
                    people[count_people].set_workplace(node.id)
                elif type_a == Type.HOME:
                    people[count_people].set_home(node.id)
                elif type_a == Type.SCHOOL:
                    people[count_people].set_school(node.id)
                count_people += 1
                people_assignment += 1
            if not is_empty:
                self.city.add_node(type_a, node)
        return determine_num+count


    def generate_population(self, individuals):
        population = []
        i = 1
        while individuals > 0:
            rand = random.randint(0, 100)
            if 0 <= rand < 25:
                aux = Person.Person(i, 'student')
                population.append(aux)
                self.students.append(aux)
            elif 25 <= rand < 80:
                aux = Person.Person(i, 'worker')
                population.append(aux)
                self.workers.append(aux)
            else:
                aux = Person.Person(i, 'elderly')
                population.append(aux)
                self.elderly.append(aux)
            individuals = individuals - 1
            i = i + 1
        return population
