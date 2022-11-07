import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tflearn
from nltk.corpus import stopwords
import tensorflow
import random
import json
import pickle

stopwords = set(stopwords.words('english'))
user_name = ''
context = ['']#determines what intents can be used
bye = False

class User:
    def __init__(self, name):
        self.name = name
        self.likes = []
        self.dislikes = []

def matching_context(lst):
    global context
    for cntxt in lst:
        if cntxt in context:
            return True
    return False
#tokenize a sentence, then lemmatize and lowercase only letters and not stopwords
def clean_sentence(sent):
    sent_words = word_tokenize(sent)

    stemmer = LancasterStemmer()
    sent_words = [stemmer.stem(word.lower()) for word in sent_words if word.isalpha() and word not in stopwords]

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
    #print(f'sent: {sent}')
    err_margin = 0.25

    model_results = model.predict([bag_of_words(sent,words)])[0]
    model_results = [[i,r] for i,r in enumerate(model_results) if r > err_margin]

    model_results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for result in model_results:
        return_list.append((classes[result[0]], result[1]))
    print(f'return list: {return_list}')
    return return_list

#determine the intent, then check down the list of intents for matching contexts, update context accordingly, respond with a random choice from the intent
def response(sent):
    global context
    global bye

    #print(f'current context: {context}')
    response_results = classify(sent)
    #print(f'response results: {response_results}')
    if response_results: #matching/probably responses for input
        while response_results: #each intent in the predicted results
            for intent in intents['intents']:
                if intent['tag'] == response_results[0][0]: #find the intent
                    #print('intent',intent)
                    #print('context_req: ',intent['context_req'])

                    if matching_context(intent['context_req']) or intent['context_req'] == [""]:    #check if we have a valid context
                        #print('current tag: ', intent['tag'])
                        context = intent['context_set']     #change/update the conversation's context
                        #print(f'context set to: {context}')
                        if intent['tag'] == 'goodbye':
                            bye = True
                            pickle.dump(user_list, open('user_list.p', 'wb'))   #save user data before exiting

                        return print(random.choice(intent['responses']))    #print a random response for the intent
            response_results.pop(0)

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
user_name = input('>>').lower()

#check for a returning user
returning_user = False
for user in user_list:
    if user_name == user.name.lower():
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
