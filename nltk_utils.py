import nltk 
# nltk.download('punkt')

from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

def tokenize(sentence):
    # This function seperate the sentence in bracket
    return nltk.word_tokenize(sentence)

def stem(word):

    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, words):
    pass

a = "What type of projects?"
print(a)

a = tokenize(a)
print(a)

words = ["Organize", "organizes", "organizing"]
stemmed_words = [ stem(w) for w in words]
print(stemmed_words)