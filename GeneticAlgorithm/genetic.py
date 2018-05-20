from deap import creator, base, tools
import random
import A_star
import game_logic
import copy
import numpy
#szansa crossover, szansa mutacji
CXPB, MUTPB = 0.5, 0.2

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
    creator.create("FitnessMulti", base.Fitness, weights=(-100.0, 1.0, -10.0))

    #this registers hall of fame
    hof = tools.HallOfFame(3)
    creator.create("Individual", list, fitness=creator.FitnessMulti)
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
    stats.register("avg", numpy.mean, axis=0)

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
    pop = toolbox.population(n=350)

    print("GENETIC LOG: PREPARED THE GENETIC ALGORITHM")

    #evaluates the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    fits = [ind.fitness.values for ind in pop]

    generation_count = 1
    record = stats.compile(pop)
    print(record)
    print("GENETIC LOG: SIMULATED SCORES OF {} GEN".format(generation_count))
    hof.update(pop)

    #evolution loop
    while generation_count < 100 and fit[0] > 0 and fit[2] > 0:
        generation_count += 1

        #Select new generation
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]): #spółkowanie pierwszej połowy z drugą z wybranych
            if random.random() < CXPB: #szansa spółkowania
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values #zmienia fitness na nieistniejący dzieci

        for mutant in offspring:
            if random.random() < MUTPB: #szansa mutacji
                toolbox.mutate(mutant)
                del mutant.fitness.values #zmienia fitness na nieistniejący tych, którzy mutated

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring #nowa populacja zamiast starej
        record = stats.compile(pop)
        hof.update(pop)
        print(record)
        print("GENETIC LOG: SIMULATED SCORES OF {} GEN".format(generation_count))
        print("Best three ever to live: ", hof)
        #LogicEngine.play_from_list(hof[0])






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
        return 100000, 0, 100000

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
