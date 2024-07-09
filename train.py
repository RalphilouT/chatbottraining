import json
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

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

disregard_w = ['?', "!", ".", ","]
every_word = [stem(w) for w in every_word if w not in disregard_w]
every_word = sorted(set(every_word))
tags = sorted(set(tags))

xword_train = []
ytag_train = []

for(pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, every_word)
    xword_train.append(tag)

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

batch_size = 8
dataset = ChatBotDataset()
train_dataloader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    