from deap import creator, base, tools, algorithms
import random
import A_star
import game_logic
import copy
import numpy
import knowledge_frames
import pickle
import multiprocessing
import itertools


#szansa crossover, szansa mutacji
CXPB, MUTPB = 0.5, 0.2

def set_creator(cr):
    global creator
    creator = cr


set_creator(creator)
creator.create("FitnessMulti", base.Fitness, weights=(-100.0, 1.0, -10.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

def set_creator(cr):
    global creator
    creator = cr

def prepare_genetic(LogicEngine):
    """
    prepares the genetic algorithm using the deap library
    :param LogicEngine:
    :return:
    """
    #1: count of enemies,
    #2 : my_own hp
    #3 : number of enemy hp
    #fitness function that aims to minimize first objective, and maximize the second, minimize the third
    #creator.create("FitnessMulti", base.Fitness, weights=(-100.0, 1.0, -10.0))

    #this registers hall of fame
    hof = tools.HallOfFame(5)
    #creator.create("Individual", list, fitness=creator.FitnessMulti)
    #individual with genes of the form of list, that take previously defined fitness function
    toolbox = base.Toolbox()

    #registers function that generates genes
    max_gene_value = len(LogicEngine.monsters + LogicEngine.mixtures)
    toolbox.register("attr_int", random.randrange, 0, max_gene_value,  1)

        #registers how to make an individual
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_int,  len(LogicEngine.monsters + LogicEngine.mixtures) * 3)


    #register statistics
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg #1 count of enemies * 100 | #2 player hp | enemy hp total * 10", numpy.mean, axis=0)
    stats.register("std #1 count of enemies * 100 | #2 player hp | enemy hp total * 10", numpy.std, axis=0)
    stats.register("min #1 count of enemies * 100 | #2 player hp | enemy hp total * 10", numpy.min, axis=0)
    stats.register("max #1 count of enemies * 100 | #2 player hp | enemy hp total * 10", numpy.max, axis=0)

    #this registers the way to select from population to crossover
    #tournament selection, choose random from population, run tournaments based on fitness score, winner goes through
    # tak naprawdę probabilistycznie wybiera: wybierz z szansą #1 że najlepszy wygra
    # wybierz z szansą mniejszą że drugi wygra..
    # słabsi przechodzą i jest diversity bo tournament size jest ograniczony, to znaczy że może być np
    # 15 najsłabszych wybranych, i 15- najsłabszy wtedy przejdzie dalej
    # https://en.wikipedia.org/wiki/Tournament_selection
    toolbox.register("select", tools.selTournament, tournsize=15)


    #registers how to mate
    # wybiera dwa punkty na stringu (liście) DNA.
    toolbox.register("mate", tools.cxTwoPoint)

    #registers how to mutate
    #szansa mutacji to indpb
    #metoda to: szansa indpb że dla atrybutu wylosuje nowy z przedziału)
    toolbox.register("mutate", tools.mutUniformInt, low= 0, up = max_gene_value - 1, indpb=0.05)
    #registers evaluate function
    toolbox.register("evaluate", evaluate_state_after_moves, LogicEngine = LogicEngine)
    #registers how to make a population
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    #create population of 300
    pop = toolbox.population(n=300)



    #multiprocessing
    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)
    #
    # print("GENETIC LOG: PREPARED THE GENETIC ALGORITHM")
    #
    # #evaluates the entire population
    # fitnesses = list(map(toolbox.evaluate, pop))
    # for ind, fit in zip(pop, fitnesses):
    #     ind.fitness.values = fit
    # fits = [ind.fitness.values for ind in pop]
    #
    # generation_count = 1
    # record = stats.compile(pop)
    # print(record)
    # print("GENETIC LOG: SIMULATED SCORES OF {} GEN".format(generation_count))
    # hof.update(pop)

    # #evolution loop
    # while generation_count < ngen and fit[0] > 0 and fit[2] > 0:
    #     generation_count += 1
    #
    #     #Select new generation
    #     offspring = toolbox.select(pop, len(pop))
    #     # Clone the selected individuals
    #     offspring = list(map(toolbox.clone, offspring))
    #
    #     # Apply crossover and mutation on the offspring
    #     for child1, child2 in zip(offspring[::2], offspring[1::2]): #spółkowanie pierwszej połowy z drugą z wybranych
    #         if random.random() < CXPB: #szansa spółkowania
    #             toolbox.mate(child1, child2)
    #             del child1.fitness.values
    #             del child2.fitness.values #zmienia fitness na nieistniejący dzieci
    #
    #     for mutant in offspring:
    #         if random.random() < MUTPB: #szansa mutacji
    #             toolbox.mutate(mutant)
    #             del mutant.fitness.values #zmienia fitness na nieistniejący tych, którzy mutated
    #
    #     # Evaluate the individuals with an invalid fitness
    #     invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    #     fitnesses = map(toolbox.evaluate, invalid_ind)
    #     for ind, fit in zip(invalid_ind, fitnesses):
    #         ind.fitness.values = fit
    #
    #     pop[:] = offspring #nowa populacja zamiast starej
    #     record = stats.compile(pop)
    #     hof.update(pop)
    #     print(record)
    #     print("GENETIC LOG: SIMULATED SCORES OF {} GEN".format(generation_count))
    #     print("Best three ever to live: ", hof)


    # number of gens to go through
    ngen = 0
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=ngen,
                                   stats=stats, halloffame=hof, verbose=True)
    print(hof)
    knowledge_frames.__save_to_file__(str(log), "gen_outcome_{}".format(ngen))
    knowledge_frames.__save_to_file__("\n" + str(hof), "gen_outcome_{}".format(ngen), newFile=False)
    knowledge_frames.__save_to_file__("\n" + (str(get_fitness_for_hof(hof, LogicEngine))), "gen_outcome_{}".format(ngen), newFile=False)

    print(get_fitness_for_hof(hof, LogicEngine))
    wait = input("Pokaż zwycięzcę: ")
    LogicEngine.play_from_list(hof[0])



def get_fitness_for_hof(hof, LogicEngine):
    return [winner.fitness.values for winner in hof]

def evaluate_state_after_moves(individual, LogicEngine):
    """
    function that evaluates individual's fitness socre
    :param individual:
    :return:
    """
    simulated_logic_engine = simulate_from_list(individual, LogicEngine)
    count_of_alive_enemies = simulated_logic_engine.alive_monsters_count()
    player_hp = simulated_logic_engine.player.hp
    sum_of_enemy_hp = simulated_logic_engine.get_all_hp()
    if(player_hp > 0):
        return count_of_alive_enemies, player_hp, sum_of_enemy_hp
    else:
        return 1000000000, 0, 10000000000

def simulate_from_list(list_of_indexes_of_objects_to_visit, LogicEngine):
    """
    simulates the game from starting LogicEngine Position using the list of objects in order to visit
    :param LogicEngine: starting state of LogicEngine
    :param list_of_indexes_of_objects_to_visit:
    :return:
    """
    original_object_list = copy.deepcopy(LogicEngine.original_object_list)
    simulated_logic_engine = LogicEngine
    for index in list_of_indexes_of_objects_to_visit:
        if(simulated_logic_engine.get_list_of_all_objects()[index].alive == True
        and [simulated_logic_engine.get_list_of_all_objects()[index].x, simulated_logic_engine.get_list_of_all_objects()[index].y] in simulated_logic_engine.get_all_available_targets()):
            simulated_logic_engine = simulated_logic_engine.simulate_move_absolute_coordinate(save_simulated_state_JSON = False, x = simulated_logic_engine.get_list_of_all_objects()[index].x, y = simulated_logic_engine.get_list_of_all_objects()[index].y)
            if(simulated_logic_engine.alive_monsters_count() == 0 or simulated_logic_engine.player.hp <= 0):
                break
    return simulated_logic_engine
