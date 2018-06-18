import numpy as np
from math import exp
import random
from game import *
from settings import *

def sigmoid(x):
    return 1/(1 + exp(-x))

def crossover(NN_1, NN_2, prob=0.3, type="neurons", logs=True):
    #type - ['neurons', 'weights']

    out_1 = NeuralNetwork(NN_1.inputs, NN_1.hidden_layer, NN_1.possible_states, zeros=True, logs=False)
    out_2 = NeuralNetwork(NN_2.inputs, NN_2.hidden_layer, NN_2.possible_states, zeros=True, logs=False)

    if type == "neurons":
        for i in range(NN_1.input_weights.shape[0]):
            if random.random() < prob:
                if logs: print("[crossover] #log swap input weight at ",i)
                out_1.input_weights[i] = np.array(NN_2.input_weights[i])
                out_2.input_weights[i] = np.array(NN_1.input_weights[i])
            else:
                out_1.input_weights[i] = np.array(NN_1.input_weights[i])
                out_2.input_weights[i] = np.array(NN_2.input_weights[i])
        if NN_1.hidden_layer != 0:
            for i in range(NN_1.layer_weights.shape[0]):
                if logs: print("[crossover] #log swap layer weight at ",i)
                if random.random() < prob:
                    out_1.layer_weights[i] = np.array(NN_2.layer_weights[i])
                    out_2.layer_weights[i] = np.array(NN_1.layer_weights[i])
                else:
                    out_1.layer_weights[i] = np.array(NN_1.layer_weights[i])
                    out_2.layer_weights[i] = np.array(NN_2.layer_weights[i])
    elif type == "weights":
        for i in range(NN_1.input_weights.shape[0]):
            for j in range(NN_1.input_weights.shape[1]):
                if random.random() < prob:
                    out_1.input_weights[i][j] = np.array(NN_2.input_weights[i][j])
                    out_2.input_weights[i][j] = np.array(NN_1.input_weights[i][j])
                else:
                    out_1.input_weights[i][j] = np.array(NN_1.input_weights[i][j])
                    out_2.input_weights[i][j] = np.array(NN_2.input_weights[i][j])
        if NN_1.hidden_layer != 0:
            for i in range(NN_1.layer_weights.shape[0]):
                for j in range(NN_1.layer_weights.shape[1]):
                    if random.random() < prob:
                        out_1.layer_weights[i][j] = np.array(NN_2.layer_weights[i][j])
                        out_2.layer_weights[i][j] = np.array(NN_1.layer_weights[i][j])
                    else:
                        out_1.layer_weights[i][j] = np.array(NN_1.layer_weights[i][j])
                        out_2.layer_weights[i][j] = np.array(NN_2.layer_weights[i][j])
    elif type == "means":
        for i in range(NN_1.input_weights.shape[0]):
            for j in range(NN_1.input_weights.shape[1]):
                out_1.input_weights[i][j] =  (NN_1.input_weights[i][j] + NN_2.input_weights[i][j]) / 2
                out_2.input_weights[i][j] =  (NN_1.input_weights[i][j] + NN_2.input_weights[i][j]) / 2

        if NN_1.hidden_layer != 0:
            for i in range(NN_1.layer_weights.shape[0]):
                for j in range(NN_1.layer_weights.shape[1]):
                    out_1.layer_weights[i][j] =  (NN_1.layer_weights[i][j] + NN_2.layer_weights[i][j]) / 2
                    out_2.layer_weights[i][j] =  (NN_1.layer_weights[i][j] + NN_2.layer_weights[i][j]) / 2

    else:
        print("[crossover] #error unknown type: '", type,"'")
    return [out_1, out_2]



def mutation(NN, prob=0.05, logs=True):
    for i in range(NN.input_weights.shape[0]):
        for j in range(NN.input_weights.shape[1]):
            if random.random() < prob:
                if logs: print("[mutation] #log mutate at ",i,j)
                # temp_change = NN.input_weights[i][j] * 0.3
                # if random.random() < 0.5:
                #     NN.input_weights[i][j] -= temp_change
                # else:
                #     NN.input_weights[i][j] += temp_change
                if random.random() < 0.5:
                    NN.input_weights[i][j] = 4*random.random() - 2
                else:
                    NN.input_weights[i][j] *= -1
    if NN.hidden_layer != 0:
        for i in range(NN.layer_weights.shape[0]):
            for j in range(NN.layer_weights.shape[1]):
                if random.random() < prob:
                    if logs: print("[mutation] #log mutate at ",i,j)
                    # temp_change = NN.input_weights[i][j] * 0.3
                    # if random.random() < 0.5:
                    #     NN.input_weights[i][j] -= temp_change
                    # else:
                    #     NN.input_weights[i][j] += temp_change
                    if random.random() < 0.5:
                        NN.layer_weights[i][j] = 4*random.random() - 2
                    else:
                        NN.layer_weights[i][j] *= -1
    return NN


class NeuralNetwork:
    def __init__(self, no_inputs, no_hidden_layer_neurons, no_possible_states, function="sig", logs=True, zeros=False):
        self.logs = logs
        self.inputs = no_inputs
        self.outputs = 4
        self.hidden_layer = no_hidden_layer_neurons
        self.possible_states = no_possible_states
        if no_hidden_layer_neurons != 0:
            if zeros:
                self.input_weights = 2*np.zeros((no_hidden_layer_neurons, no_inputs * no_possible_states + 1)) - 1
                self.layer_weights = 2*np.zeros((self.outputs, no_hidden_layer_neurons + 1)) - 1
            else:
                self.input_weights = 2*np.random.random((no_hidden_layer_neurons, no_inputs * no_possible_states + 1)) - 1
                self.layer_weights = 2*np.random.random((self.outputs, no_hidden_layer_neurons + 1)) - 1
        else:
            if zeros:
                self.input_weights = 2*np.zeros((self.outputs, no_inputs * no_possible_states + 1)) - 1
                self.layer_weights = 2*np.zeros((self.outputs, no_hidden_layer_neurons + 1)) - 1
            else:
                self.input_weights = 2*np.random.random((self.outputs, no_inputs * no_possible_states + 1)) - 1
                self.layer_weights = 2*np.random.random((self.outputs, no_hidden_layer_neurons + 1)) - 1

        self.function = function

    def set_weights(self):
        pass

    def save_to(self, path):
        all_data = np.array([self.input_weights, self.layer_weights, self.inputs, self.outputs, self.hidden_layer, self.possible_states, self.function])
        np.save(path, all_data)
        print("[save] #log neural networks saved to'" + path + "'")

    def load_from(self, path):
        all_data = np.load(path)
        print("[load] #log try to load neural networks from'" + path + "'")
        self.input_weights = all_data[0]
        self.layer_weights = all_data[1]
        self.inputs = all_data[2]
        self.outputs = all_data[3]
        self.hidden_layer = all_data[4]
        self.possible_states = all_data[5]
        self.function = all_data[6]
        print("[load] #log loaded")

    def parse_input(self, input_from_game):
        out = np.array([])
        for row in input_from_game:
            for i in row:
                if i == -1: continue
                temp_in = np.zeros(self.possible_states)
                temp_in[i] = 1
                out = np.append(out, temp_in)
        return out.flatten()

    def evaluate(self, input_from_game):
        input = np.append(self.parse_input(input_from_game), [1]) #np array
        if self.logs: print("[evaluate] #log: expected no inputs:",self.inputs * self.possible_states + 1)
        if self.logs: print("[evaluate] #log: no inputs:",len(input))
        if len(input) != self.inputs * self.possible_states + 1:
            if self.logs: print("[evaluate] #error: bad amount of inputs for NN")
            return -1
        # print("[evaluate] #log: inputs: ", input)

        # print(self.input_weights.shape)
        # print(self.layer_weights.shape)

        layer = np.empty(self.hidden_layer)
        for neuron_num in range(self.hidden_layer):
            weighted_sum = 0
            for i in range(len(input)):
                weighted_sum += input[i] * self.input_weights[neuron_num][i]
            layer[neuron_num] = sigmoid(weighted_sum)
        layer = np.append(layer, [1])
        if self.logs: print("[evaluate] #log: hidden layer outputs: ",layer.shape)

        output = np.empty(self.outputs) #[UP, DOWN, RIGHT, LEFT]
        # print(self.layer_weights.shape)
        for o in range(self.outputs):
            weighted_sum = 0
            for l in range(len(layer)):
                weighted_sum += layer[l] * self.layer_weights[o][l]
            output[o] = sigmoid(weighted_sum)
        if self.logs: print("[evaluate] #log: network output: ", output)
        return output

    def evaluate_no_hidden_layer(self, input_from_game):
        # print("from game",input_from_game)
        input = np.append(self.parse_input(input_from_game), [1])
        # print("NN input",input)
        if self.logs: print("[evaluate] #log: expected no inputs:",self.inputs * self.possible_states + 1)
        if self.logs: print("[evaluate] #log: no inputs:",len(input))
        if len(input) != self.inputs * self.possible_states + 1:
            if self.logs: print("[evaluate] #error: bad amount of inputs for NN")
            return -1

        output = np.empty(self.outputs) #[UP, DOWN, RIGHT, LEFT]
        for o in range(self.outputs):
            weighted_sum = 0
            for i in range(len(input)):
                weighted_sum += input[i] * self.input_weights[o][i]
            output[o] = sigmoid(weighted_sum)
        if self.logs: print("[evaluate] #log: network output: ", output)
        return output



# test
# nn = NeuralNetwork(8,10,3)
# nn.save_to('data/networks/1.npy')
# load_nn = NeuralNetwork(8,10,3)
# load_nn.load_from('data/networks/1.npy')
# out = crossover(nn, load_nn)
# nn_1_2 = NeuralNetwork(8,10,3)
# print(nn_1_1.input_weights.shape)
# print(nn_1_1.layer_weights.shape)
# print(crossover(nn_1_1, nn_1_2))
# print(mutation(nn_1_1))
#
# print("------")
#
# nn_2_1 = NeuralNetwork(8,0,3)
# nn_2_2 = NeuralNetwork(8,0,3)
# print(nn_2_1.input_weights.shape)
# # print(nn_2_1.layer_weights)
# print(crossover(nn_2_1, nn_2_2))
# print(mutation(nn_2_1))

def train_network(screen):
    print("------START NETWORK TRAINING-------")
    neural_network = NeuralNetwork(NN_INPUTS, NN_HIDDEN_LAYER_SIZE, NN_POSSIBLE_STATES, logs = True)
    game = Game(screen, 'neural-networks-treining')
    game.set_network(neural_network)
    print("SCORE: ", game.run())
    # screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
    # # network = NeuralNetwork(1,1,1)
    # # network.load_from('data/networks/best.npy')
    # # game = Game(screen, False, logs = False)
    # # game.set_mode("auto-neural-network", MOVES)
    # # game.set_network(network)
    # # print("SCORE: ", game.run())
    #
    #
    # outfile = io.open(FILENAME, 'w+')
    # outfile.write("#TYPE: sigmoid\n#GENERATION SIZE: "+str(GENERATION_SIZE)+"\n#MAX GENERATIONS: " + str(ROUNDS) + "\n#INPUTS: "+str(INPUTS)+"\n")
    # outfile.write("#MUTATION PROB: " + str(MUTATION_PROB) + "\n#CROSS PROB:" + str(CROS_PROB) + "\n#CROSS_TYPE: " + CROSS_TYPE + "\n#MOVES: "+str(MOVES)+"\n#HIDDEN LAYER SIZE: "+str(HIDDEN_LAYER_SIZE) + "\n")
    # # game = Game(screen, False, logs = False)
    # # game.set_mode("auto-neural-network", MOVES)
    # # neural_network = NeuralNetwork(INPUTS, HIDDEN_LAYER_SIZE, POSSIBLE_STATES, logs = True)
    # # neural_network.load_from("data/networks/best.npy")
    # # # neural_network.input_weights[0][3] = -10
    # # # neural_network.input_weights[1][18] = -10
    # # # neural_network.input_weights[2][12] = -10
    # # # neural_network.input_weights[3][9] = -10
    # # game.set_network(neural_network)
    # # fitness_score = game.run()
    # # print(fitness_score)
    #
    #
    # # init generation #0
    # generation = []
    # fitness_sum = 0
    # for i in range(GENERATION_SIZE):
    #     print("[program] #log evaluate game: ",i)
    #     game = Game(screen, True, logs = False)
    #     game.set_mode("neural-network", MOVES)
    #     new_network = NeuralNetwork(INPUTS, HIDDEN_LAYER_SIZE, POSSIBLE_STATES, logs = False)
    #     game.set_network(new_network)
    #     fitness_score = game.run()
    #     print(fitness_score)
    #     generation.append([new_network, fitness_score])
    #     fitness_sum += fitness_score
    #
    #     game = Game(screen, True, logs = False)
    #     game.set_mode("neural-network", MOVES)
    #     game.set_network(generation[i][0])
    #     fitness_score = game.run()
    #     # print(fitness_score)
    #
    # # generation #0 summary
    # print("-----\n[program] #log generation ", 0)
    # print("[program] #log score of generation: ", fitness_sum)
    # max_score = 0
    # max_index = -1
    # for i in range(GENERATION_SIZE):
    #     if(max_score < generation[i][1]):
    #         max_score = generation[i][1]
    #         max_index = i
    # print("[program] #log best: ", max_index , max_score,"\n-----")
    # # outfile = io.open(FILENAME, 'w+')
    # outfile.write(str(0) + " " + str(max_score) + " " + str(fitness_sum // GENERATION_SIZE) + "\n")
    # # outfile.close()
    # # print(max_index, generation[max_index][1])
    # # generation[max_index][1] *= 4
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
