import random
import json
import torch
from model import Net
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f: 
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
every_words = data["every_words"]
tags = data["tags"]
model_state = data["model_state"]


model = Net(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Ralph"

def get_response(user_input):
    sentence = tokenize(user_input)
    X = bag_of_words(sentence, every_words)
    # Model expects it to be this form  with 1 row  (due to 1 sample)
    X = X.reshape(1, X.shape[0])
    # Convert to torch tensor,  bog returns numpy array
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probability = torch.softmax(output, dim=1)
    prob = probability[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    else: 
        return "I do not understand..."

if __name__ == "__main__":
    print("Let's chat! type quit to exit")
    while True:
        sentence = input('You: ')
        if sentence == "quit":
            break

        bot_response = get_response(sentence)
        print(f'{bot_name}: {bot_response}')
