import numpy as np
import random
from math import exp

def sigmoid(x):
    return 1/(1 + exp(-x))

class NeuralNetwork:
    def __init__(self, no_inputs, no_hidden_layer_neurons, no_possible_states, function="sig"):
        self.inputs = no_inputs
        self.outputs = 4
        self.hidden_layer = no_hidden_layer_neurons
        self.possible_states = no_possible_states
        self.input_weights = 2*np.random.random((no_hidden_layer_neurons, no_inputs * no_possible_states + 1)) - 1
        self.layer_weights = 2*np.random.random((self.outputs, no_hidden_layer_neurons + 1)) - 1
        self.function = function

    def set_weights(self):
        pass

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
        if len(input) != self.inputs * self.possible_states + 1:
            print("[evaluate] #error: bad amount of inputs for NN")
            return -1
        print("[evaluate] #log: inputs: ", input)

        print(self.input_weights.shape)
        print(self.layer_weights.shape)
        
        layer = np.empty(self.hidden_layer)
        for neuron_num in range(self.hidden_layer):
            weighted_sum = 0
            for i in range(len(input)):
                weighted_sum += input[i] * self.input_weights[neuron_num][i]
            layer[neuron_num] = sigmoid(weighted_sum)
        layer = np.append(layer, [1])
        print(layer.shape)

        output = np.empty(self.outputs) #[UP, DOWN, RIGHT, LEFT]
        # print(self.layer_weights.shape)
        for o in range(self.outputs):
            weighted_sum = 0
            for l in range(len(layer)):
                weighted_sum += layer[l] * self.layer_weights[o][l]
            output[o] = sigmoid(weighted_sum)
        return output



#test
new_network = NeuralNetwork(8,10,3)
print(new_network.evaluate([[ 0,  0, 0], [ 0, -1 , 1],[ 0 , 1 , 1]]))
