import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy
import tflearn
import tensorflow
import random
import json
import pickle

with open('../intents.json') as json_data:
    intents = json.load(json_data)

words = [] #holds all words derived from patterns (lemmatized)
classes = []
documents = [] #corpus of words under specific intents
ignore_punct = ['?', '.', '!']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        #print(f"working on intent '{intent['tag']}'")
        pattern_words = word_tokenize(pattern)

        words.extend(pattern_words)

        documents.append((pattern_words, intent['tag']))

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#lemmatize and lowercase each word
lemmatizer = WordNetLemmatizer()
words = [lemmatizer.lemmatize(pattern_words.lower()) for pattern_words in words if pattern_words not in ignore_punct]

#remove duplicates
words = sorted(set(words))
classes = sorted(set(classes))

#print(f'number of documents {len(documents)}')
#print(f'number of classes {len(classes)} ', classes)
#print(f'unique lemmas {len(words)}', words)

training = []
training_out = []

empty_arr = [0] * len(classes)

for document in documents:

    bag_of_words = []
    pattern_words = document[0]

    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]

    for word in words:
        if word in pattern_words:
            bag_of_words.append(1)
        else:
            bag_of_words.append(0)

    output_row = list(empty_arr)
    output_row[classes.index(document[1])] = 1

    training.append([bag_of_words, output_row])


#shuffle
random.shuffle(training)
training = numpy.array(training)

train_x = list(training[:,0])
train_y = list(training[:,1])

tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation = 'softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
model.fit(train_x, train_y, n_epoch=500, batch_size=8, show_metric=True)
model.save('model.tflearn')

pickle.dump({'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open("training_data", "wb"))
