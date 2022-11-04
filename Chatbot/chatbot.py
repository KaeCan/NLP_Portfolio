import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize.treebank import TreebankWordDetokenizer
import numpy
import tflearn
import tensorflow
import random
import json
import pickle

stopwords = set(stopwords.words('english'))
user_name = ''
context = [""] #determines what intents can be used
bye = False

class User:
    def __init__(self, name):
        self.name = name
        self.likes = []
        self.dislikes = []


#tokenize a sentence, then lemmatize and lowercase only letters and not stopwords
def clean_sentence(sent):
    sent_words = word_tokenize(sent)

    lemmatizer = WordNetLemmatizer()
    sent_words = [lemmatizer.lemmatize(word.lower()) for word in sent_words if word.isalpha() and word not in stopwords]

    return sent_words

#clean sentence, mark which words are present in the input
def bag_of_words(sent, words):
    sent_words = clean_sentence(sent)
    bag = [0] * len(words)
    for s in sent_words:
        for i,word in enumerate(words):
            if word == s:
                bag[i] = 1

    return(numpy.array(bag))

#predict the intent using a bag of words, return a descending list of probable responses
def classify(sent):
    err_margin = 0.25

    results = model.predict([bag_of_words(sent,words)])[0]
    results = [[i,r] for i,r in enumerate(results) if r > err_margin]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for result in results:
        return_list.append((classes[result[0]], result[1]))
    return return_list

#determine the intent, then check down the list of intents for matching contexts, update context accordingly, respond with a random choice from the intent
def response(sent):
    results = classify(sent)

    if results: #matching/probably responses for input
        while results:
            for intent in intents['intents']: #each intent in the predicted results
                if intent['tag'] == results[0][0]: #match the tag of the next top intent
                    #if intent['context_filter'] in context:
                    #    context[user] = intent['context_set']
                    #if intent['context_filter'] != "" or (user in context and intent['context_filter'] == context[user]):
                    #    return print(random.choice(intent['responses']))

                    if intent['context_req'] in context or intent['context_req'] == "":    #check if we have a valid context
                        context = intent['context_set']     #change/update the conversation's context
                        if intent['tag'] == 'goodbye':
                            bye = True
                            pickle.dump(user_list, open('user_list.p', 'wb'))   #save user data before exiting

                        return print(random.choice(intent['responses']))    #print a random response for the intent
            results.pop(0)

def greet_user():
    #get greeting intent
    for intent in intents['intents']:
        if intent['tag'] == 'greeting':
            return print(random.choice(intent['responses']))

def welcome_back_user():
    #get welcome back intent
    for intent in intents['intents']:
        if intent['tag'] == 'welcomeback':
            return print(random.choice(intent['responses']))

#----Main----
#open intents file
with open('intents.json') as json_data:
    intents = json.load(json_data)

#load in our model's training data
data = pickle.load(open('model/training_data', 'rb'))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

#set up neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation = 'softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)
#load model
model.load('model/model.tflearn')

#load users
user_list = pickle.load(open('user_list.p', 'rb'))

#BEGIN conversation by asking for name
print("May I ask for you name please?")
user_name = input('>>')

#check for a returning user
returning_user = False
for user in user_list:
    if user_name in user.name:
        current_user = user #set the current user based off the user list
        welcome_back_user()
        returning_user = True
        break

if not returning_user:
    current_user = User(user_name) #create a new user
    user_list.append(user)
    greet_user()


while not bye:
    user_in = input('>>')
    response(user_in)
