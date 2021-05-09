import random
import Person


class Simulation:
    def __init__(self, individuals, incubation, symptomatic, immunity, mortality, beacons):
        self.population = self.generate_population(individuals)
        self.incubation = incubation
        self.symptomatic = symptomatic
        self.immunity = immunity
        self.mortality = mortality

    @staticmethod
    def generate_population(individuals):
        population = []
        i = 1
        while individuals > 0:
            rand = random.randint(0, 100)
            if 0 <= rand < 25:
                population.append(Person.Person(i, 'student'))
            elif 25 <= rand < 80:
                population.append(Person.Person(i, 'worker'))
            else:
                population.append(Person.Person(i, 'elderly'))
            individuals = individuals - 1
            i = i + 1
        return population
