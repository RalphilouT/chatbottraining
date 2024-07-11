import json
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from model import Net

with open('intents.json','r') as f:
    intents = json.load(f)

# print(intents)

every_word = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        #using extend since w is array
        every_word.extend(w)
        xy.append((w, tag))

disregard_w = ['?', "!", "."]
every_word = [stem(w) for w in every_word if w not in disregard_w]
every_word = sorted(set(every_word))
tags = sorted(set(tags))

xword_train = []
ytag_train = []

for(pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, every_word)
    xword_train.append(bag)

    # Numbers for labels
    label = tags.index(tag)
    ytag_train.append(label)

xword_train = np.array(xword_train)
ytag_train = np.array(ytag_train)

class ChatBotDataset(Dataset):
    def __init__(self):
        self.n_samples = len(xword_train)
        self.x_data = xword_train
        self.y_data = ytag_train
    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples

# Parameters
batch_size = 8
# layer 
hidden_size = 8
# Number of tags/class 
output_size = len(tags)
# Length of bag of words or every_word 
input_size = len(xword_train[0])
learning_rate = 0.001
num_epochs = 1000

dataset = ChatBotDataset()
train_dataloader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = Net(input_size, hidden_size, output_size).to(device)

#loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Training loop 
for epoch in range(num_epochs):
    for(words, labels) in train_dataloader:
        words = words.to(device)
        # labels = labels.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        # forward pass 
        outputs = model(words)
        loss = criterion(outputs, labels)

        # backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    if(epoch +1) % 100 == 0:
        print(f'epoch {epoch +1}/{num_epochs}, loss ={loss.item():.4f}')

print(f'final loss, loss ={loss.item():.4f}')

# Save data 
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "every_words": every_word,
    "tags" : tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. saved to {FILE}')