import math
import random

random.seed(1)


def create_random_number(a, b):
    return (b - a) * random.random() + a


def create_matrix(m, n, fill=0.0):
    mat = []
    for i in range(m):
        mat.append([fill] * n)
    return mat


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


class BPNN:
    def __init__(self):
        # init numbers of all layers
        self.input_n = 0
        self.hidden_n = 0
        self.output_n = 0
        # init all layers matrix
        self.input_cells = []
        self.hidden_cells = []
        self.output_cells = []
        # init weight matrix
        self.input_weights = []
        self.output_weights = []
        # init correct matrix
        self.input_correct = []
        self.output_correct = []

    def setup(self, _input_n, _hidden_n, _output_n):
        self.input_n = _input_n + 1
        self.hidden_n = _hidden_n
        self.output_n = _output_n
        # init all layers cells
        self.input_cells = [1.0] * self.input_n
        self.hidden_cells = [1.0] * self.hidden_n
        self.output_cells = [1.0] * self.output_n
        # init weights matrix
        self.input_weights = create_matrix(self.input_n, self.hidden_n)
        self.output_weights = create_matrix(self.hidden_n, self.output_n)
        # give weight matrix random numbers
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                self.input_weights[i][h] = create_random_number(-0.2, 0.2)
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                self.output_weights[h][o] = create_random_number(-2.0, 2.0)
        # init correction matrix
        self.input_correct = create_matrix(self.input_n, self.hidden_n)
        self.output_correct = create_matrix(self.hidden_n, self.output_n)

    def predict(self, inputs):
        # activate input layer
        for i in range(self.input_n - 1):
            self.input_cells[i] = inputs[i]
        # matrix dot active hidden layer
        for j in range(self.hidden_n):
            total = 0.0
            for i in range(self.input_n):
                total += self.input_cells[i] * self.input_weights[i][j]
            self.hidden_cells[j] = sigmoid(total)
        # matrix dot active output layer
        for k in range(self.output_n):
            total = 0.0
            for j in range(self.hidden_n):
                total += self.hidden_cells[j] * self.output_weights[j][k]
            self.output_cells[k] = sigmoid(total)
        return self.output_cells[:]

    def back_propagate(self, case, label, learn, correct):
        # feed forward
        self.predict(case)
        # get output layer error
        output_deltas = [0.0] * self.output_n
        for o in range(self.output_n):
            error = label[o] - self.output_cells[o]
            output_deltas[o] = sigmoid_derivative(self.output_cells[o]) * error
        # get hidden layer error
        hidden_deltas = [0.0] * self.hidden_n
        for h in range(self.hidden_n):
            error = 0.0
            for o in range(self.output_n):
                error += output_deltas[o] * self.output_weights[h][o]
            hidden_deltas[h] = sigmoid_derivative(self.hidden_cells[h]) * error
        # update output weights
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                change = output_deltas[o] * self.hidden_cells[h]
                self.output_weights[h][o] += learn * change + \
                    correct * self.output_correct[h][o]
                self.output_correct[h][o] = change
        # update input weights
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                change = hidden_deltas[h] * self.input_cells[i]
                self.input_weights[i][h] += learn * change + \
                    correct * self.input_correct[i][h]
                self.input_correct[i][h] = change
        # get global error
        error = 0.0
        for o in range(len(label)):
            error += 0.5 * (label[o] - self.output_cells[o]) ** 2
        return error

    def train(self, cases, labels, limit, learn, correct):
        for j in range(limit):
            error = 0.0
            for i in range(len(cases)):
                label = labels[i]
                case = cases[i]
                error += self.back_propagate(case, label, learn, correct)
