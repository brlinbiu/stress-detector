import numpy as np


class NeuralNetwork():
    def __init__(self) -> None:
        np.random.seed(1)
        self.synaptic_weights = 2 * np.random.random(size=(3, 1)) - 1

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivation(self, x):
        return x * (1 - x)

    def train(self, training_inputs, training_outputs, training_iterations):
        for iteration in range(training_iterations):
            output = neural_network.think(training_inputs)
            error = training_outputs - output
            adjustments = np.dot(train_inputs.T, error *
                                 self.sigmoid_derivation(output))
            self.synaptic_weights += adjustments

    def think(self, inputs):
        inputs = inputs.astype(float)
        return self.sigmoid(np.dot(inputs, self.synaptic_weights))


neural_network = NeuralNetwork()
# print(neural_network.synaptic_weights)
train_inputs = np.array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
train_outputs = np.array([[0, 1, 1, 0]]).T
neural_network.train(training_inputs=train_inputs,
                     training_outputs=train_outputs,
                     training_iterations=150000)
# print(neural_network.synaptic_weights)
input_1 = str(input("输入第一个值: "))
input_2 = str(input("输入第一个值: "))
input_3 = str(input("输入第一个值: "))
print(neural_network.think(np.array([input_1, input_2, input_3])))
