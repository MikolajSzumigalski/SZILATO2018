import numpy as np
from math import exp
import random

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
