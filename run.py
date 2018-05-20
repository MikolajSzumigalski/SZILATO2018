#THIS FILE IS RESPONSIBLE FOR RUNNING THE PROGRAM, RUN THIS TO RUN THE APPLICATION
import program_logic
import GeneticAlgorithm
from deap import creator, base

if __name__ == "__main__":
    # set_creator(creator)
    # creator.create("FitnessMulti", base.Fitness, weights=(-100.0, 1.0, -10.0))
    # creator.create("Individual", list, fitness=creator.FitnessMulti)
    program_logic.startup()
