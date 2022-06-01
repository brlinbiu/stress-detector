"""
MBPNN Structure use PyTorch to achieve
7 input
12 1st hidden layer
10 2nd hidden layer
8 3rd hidden layer
2 output
"""
import torch

from torch import nn


class BPNNModel(torch.nn.Module):
    def __init__(self):
        super(BPNNModel, self).__init__()

        self.layer1 = nn.Sequential(nn.Linear(7, 12), nn.ReLU())
        self.layer2 = nn.Sequential(nn.Linear(12, 10), nn.ReLU())
        self.layer3 = nn.Sequential(nn.Linear(10, 8), nn.ReLU())
        self.layer4 = nn.Sequential(nn.Linear(8, 2))

    def forward(self, data):
        data = self.layer1(data)
        data = self.layer2(data)
        data = self.layer3(data)
        data = self.layer4(data)
        return data