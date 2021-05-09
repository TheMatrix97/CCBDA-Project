from simulation.Simulation import Simulation


def test():
    simulation = Simulation(1000, 2, 4, 14, 10, False, 100)
    simulation.start_simulation()
    while True:
        simulation.advance_round()



if __name__ == "__main__":
    test()
