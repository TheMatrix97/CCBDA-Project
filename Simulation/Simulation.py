import random
import Person
from simulation.City import City
from simulation.Node import Node
from simulation.Type import Type


class Simulation:
    def __init__(self, individuals, incubation, symptomatic, immunity, mortality, beacons):
        self.elderly = []
        self.workers = []
        self.students = []
        self.population = self.generate_population(individuals)
        self.incubation = incubation
        self.symptomatic = symptomatic
        self.immunity = immunity
        self.mortality = mortality
        self.city = City()
        self.generate_nodes()

    def generate_nodes(self): #Our population is assigned
        # Workplaces
        self.create_assign_nodes(Type.WORKPLACE, self.workers, 20, 40)

        # Homes
        self.create_assign_nodes(Type.HOME, self.population, 1, 5)

        # School
        self.create_assign_nodes(Type.SCHOOL, self.students, 100, 200)

        # Others
        self.create_assign_nodes(Type.OTHER, self.population, 50, 100)


    def create_assign_nodes(self, type_a, people, max_num, min_num):
        determine_num = random.randint(int(len(people) / min_num), int(len(people) / max_num))
        nodes = []
        for i in range(0, determine_num):
            node = Node(i, type_a)
            nodes.append(node)
        # Assigned people workplaces
        capacity = len(people) / len(nodes)
        count_people = 0
        for node in nodes:
            people_assignment = 0
            while people_assignment < int(capacity) and count_people < len(people):
                if type_a == Type.WORKPLACE:
                    people[count_people].set_workplace(node.id)
                elif type_a == Type.HOME:
                    people[count_people].set_home(node.id)
                elif type_a == Type.SCHOOL:
                    people[count_people].set_school(node.id)
                count_people += 1
                people_assignment += 1
            self.city.add_node(type_a, node)


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
