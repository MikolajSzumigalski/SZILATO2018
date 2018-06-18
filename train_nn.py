from game import *
from settings import *
import io


def train_network(screen):
    print("------START NETWORK TRAINING-------")
    # neural_network = NeuralNetwork(NN_INPUTS, NN_HIDDEN_LAYER_SIZE, NN_POSSIBLE_STATES, logs = True)
    # game = Game(screen, 'neural-networks-training')
    # game.set_network(neural_network)
    # game.set_max_rounds = NN_MOVES
    # print("SCORE: ", game.run())
    mode = 'neural-networks-training'

    outfile = io.open('networks/training_logs/'+NN_FILENAME, 'w+')
    outfile.write("#TYPE: sigmoid\n#GENERATION SIZE: "+str(NN_GENERATION_SIZE)+"\n#MAX GENERATIONS: " + str(NN_ROUNDS) + "\n#INPUTS: "+str(NN_INPUTS)+"\n")
    outfile.write("#MUTATION PROB: " + str(NN_MUTATION_PROB) + "\n#CROSS PROB:" + str(NN_CROS_PROB) + "\n#CROSS_TYPE: " + NN_CROSS_TYPE + "\n#MOVES: "+str(NN_MOVES)+"\n#HIDDEN LAYER SIZE: "+str(NN_HIDDEN_LAYER_SIZE) + "\n")

    # init generation #0
    generation = []
    fitness_sum = 0
    for i in range(NN_GENERATION_SIZE):
        print("[program] #log evaluate game: ",i, " score: ", end='')
        game = Game(screen, mode)
        game.set_max_rounds = NN_MOVES
        new_network = NeuralNetwork(NN_INPUTS, NN_HIDDEN_LAYER_SIZE, NN_POSSIBLE_STATES, logs = False)
        game.set_network(new_network)
        fitness_score = game.run()
        print(fitness_score)
        generation.append([new_network, fitness_score])
        fitness_sum += fitness_score

        # game = Game(screen, True, logs = False)
        # game.set_mode("neural-network", MOVES)
        # game.set_network(generation[i][0])
        # fitness_score = game.run()
        # # print(fitness_score)

    # generation #0 summary
    print("-----\n[program] #log generation ", 0)
    print("[program] #log score of generation: ", fitness_sum)
    max_score = 0
    max_index = -1
    for i in range(NN_GENERATION_SIZE):
        if(max_score < generation[i][1]):
            max_score = generation[i][1]
            max_index = i
    print("[program] #log best: ", max_index , max_score,"\n-----")
    outfile.write(str(0) + " " + str(max_score) + " " + str(fitness_sum // NN_GENERATION_SIZE) + "\n")
    generation[max_index][1] *= NN_FIRST_PRIZE
    neural_network = generation[max_index][0]
    #
    # # display best solution from generation #0
    # # game = Game(screen, False, logs = False)
    # # game.set_mode("neural-network", MOVES)
    # # game.set_network(generation[max_index][0])
    # # fitness_score = game.run()
    # # print(fitness_score)
    #
    #
    # for r in range(1,ROUNDS+1):
    #     # create mating pool from #n generation
    #     mating_pool = []
    #     for i in range(GENERATION_SIZE):
    #         generation[i].append(round(generation[i][1] / fitness_sum * 100))
    #         for j in range(generation[i][2]):
    #             mating_pool.append(i)
    #         # print(mating_pool)
    #         # print(generation[i][2])
    #
    #     # init #n+1 generation through crossovers (neural networks) based on mating pools and scores
    #     new_generation = []
    #     if CROSS_TYPE == 'means':
    #         temp_range = GENERATION_SIZE
    #     else:
    #         temp_range = GENERATION_SIZE//2
    #
    #     for i in range(temp_range):
    #         x = random.choice(mating_pool)
    #         y = random.choice(mating_pool)
    #         # print("[program] #log perform crossover of ", x,  y)
    #         new_pair = crossover(generation[x][0], generation[y][0], type=CROSS_TYPE ,prob=CROS_PROB,logs=False)
    #         new_generation.append(mutation(new_pair[0], prob=MUTATION_PROB, logs=False))
    #         if not CROSS_TYPE == 'means':
    #             new_generation.append(mutation(new_pair[1], prob=MUTATION_PROB, logs=False))
    #
    #
    #     # evaluate generation #n+1
    #     fitness_sum = 0
    #     generation = []
    #     print("[program] #log evaluate games in gen: ",r)
    #
    #     for i in range(GENERATION_SIZE):
    #         # print("[program] #log evaluate game: ",i)
    #         game = Game(screen, True, logs = False)
    #         game.set_mode("neural-network", MOVES)
    #         # new_network = NeuralNetwork(INPUTS, HIDDEN_LAYER_SIZE, POSSIBLE_STATES, logs = False)
    #         game.set_network(new_generation[i])
    #         fitness_score = game.run()
    #         generation.append([new_generation[i], fitness_score])
    #         fitness_sum += fitness_score
    #
    #     # generate summary for #n+1 generation
    #     print("-----\n[program] #log generation ", r)
    #     print("[program] #log score of generation: ", fitness_sum)
    #     max_score = 0
    #     max_index = -1
    #     for i in range(GENERATION_SIZE):
    #         if(max_score < generation[i][1]):
    #             max_score = generation[i][1]
    #             max_index = i
    #     print("[program] #log best: ", max_index , max_score,"\n-----")
    #     outfile.write(str(r) + " " + str(max_score) + " " + str(fitness_sum // GENERATION_SIZE) + "\n")
    #     generation[max_index][1] *= FIRST_PRIZE
    #     if max_score >= MOVES * 100:
    #         generation[max_index][0].save_to('data/networks/best.npy')
    #         best = NeuralNetwork(1,1,1)
    #         best.load_from('data/networks/best.npy')
    #         game = Game(screen, False, logs = False)
    #         game.set_mode("neural-network", MOVES)
    #         game.set_network(best)
    #         fitness_score = game.run()
    #         print(fitness_score)
    #         outfile.close()
    #         break
    #
    # generation[max_index][0].save_to('data/networks/best_new.npy')
    #
    #


    print("------FIN-------")
    return neural_network
