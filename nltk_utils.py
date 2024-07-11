import nltk 
# nltk.download('punkt')

from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
import numpy as np

def tokenize(sentence):
    # This function seperate the sentence in bracket
    return nltk.word_tokenize(sentence)

def stem(word):

    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    """
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    sentence_words = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype= np.float32)
    # Get index and word from all_word
    for idx, word in enumerate(all_words):
        # if tokenize sentence is in words, then acknowledge
        if word in sentence_words:
            bag[idx] = 1.0

    return bag
