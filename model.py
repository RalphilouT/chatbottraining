import torch
import torch.nn as nn

# feed forward nueral network
class Net(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(Net, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        # activiation function
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)

        # different layer
        out = self.l2(out)
        out = self.relu(out)

        # different layer
        out = self.l3(out)
        
        # no activation and no soft max
        return out

        
