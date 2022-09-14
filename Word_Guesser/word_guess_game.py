import sys
from random import seed
from random import randint
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

#diversity ratio is unique tokens / all tokens
def get_diversity_ratio(list):
    return len(set(list)) / len(list)

#helper to print underscores or letters during the game duration
def print_list(list):
    for i in list:
        print(i, end = ' ')

#helper to see if a guessed letter is part of the word in the game
def get_indices(list, char):
    indices = []
    for i in range(len(list)):
        if list[i] == char:
            indices.append(i)

    return indices

#game routine for a hangman-like game
def game_loop(word_bank):

    #start of default score and randomly select a word from our bank
    score = 5
    word = word_bank[randint(0,50)]

    #char list of the word to be guessed
    char_list = [*word]
    #a char list of letter we've guessed correctly so far
    user_list = []
    for x in range(len(word)):
        user_list.append('_')

    #debug
    #print(char_list)

    #output beginning of game
    #loop through game until no more points or fully guessed word
    print('Let\'s play a word guessing game!')
    while score > -1:
        #display word and score
        print('Score is ' + str(score))
        print_list(user_list)
        if char_list == user_list:
            print('You solved it!')
            break

        #let user choose a letter to guess
        guess = input("\nGuess a letter: ")

        #force exit
        if guess == '!':
            print('Exiting.')
            break

        #game logic
        indices = get_indices(char_list, guess)
        if indices:
            #we add the correctly guessed letters to the user's list
            for index in indices:
                user_list[index] = guess
                print('Right!', end = ' ')
        else:
            #we substract a point from user's score for incorrectly guessing
            score -= 1
            if score > -1:
                print('Sorry, guess again.', end = ' ')

    print('You failed.')
    print('\nCurrent Score: ' + str(score))

#processing routine for preparing the word bank to be used in the word guesser
def create_word_bank(raw_tokens):

    #preprocess and clean out unnecessary tokens
    tokens, nouns = preprocess(raw_tokens)

    #determine word count of each noun
    freq_dist = FreqDist(tokens)

    #nouns placed in a dictionary {key= frequency : value= [noun]}
    noun_dict = {}
    for noun in nouns:
        #frequency key is not present yet, create new entry to place new noun
        if freq_dist[noun] not in noun_dict.keys():
            noun_dict[freq_dist[noun]] = [noun]
        #add noun to already existing frequency's list association
        else:
            noun_dict[freq_dist[noun]].append(noun)

    #get all frequencies from greatest to least
    frequencies = sorted(noun_dict, reverse=True)

    #place all words into a list organized by most frequent to least
    all_bank = []
    for freq in frequencies:
        #append all nouns with the same frequency all at once
        for noun in noun_dict[freq]:
            all_bank.append(noun)

    #extract the 50 most common words and display them with their frequencies
    fifty_bank = []
    print('50 most common words:')
    for x in range(50):
        #we need the corresponding key (frequency) to the word
        #which is wrapped inside a char_list

        for list in noun_dict.values(): #find the list that has our word in it
            if all_bank[x] in list:

                for key in noun_dict: #find the key that is associated with that list
                    if noun_dict[key] == list:
                        freq = key
        #word : frequency
        print(str(all_bank[x]) + ' : ' + str(freq))
        #extract word to separate list
        fifty_bank.append(all_bank[x])

    return fifty_bank


#routine to remove all unnecessary tokens for further processing in create_word_bank()
def preprocess(raw_tokens):
    #make all lowercase
    tokens = [t.lower() for t in raw_tokens]
    #only take all tokens that are not punctuation, not stopwords, and not length 5 or less
    tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]
    #lemmatize
    lemmatizer = WordNetLemmatizer()
    lemms = [lemmatizer.lemmatize(token) for token in tokens]
    #get all unique lemmas
    unq_lemms = list(set(lemms))
    #tag the lemmas with their part-of-speech
    tag_lemms = nltk.pos_tag(unq_lemms)

    print('First 20 tagged unique lemmas:')
    for lemm in range(0,20):
        print(tag_lemms[lemm])

    #extract all the nouns from the list of tagged lemmas
    all_nouns = []
    for token, pos in tag_lemms:
        if pos == 'NN':
            all_nouns.append(token)

    print('Number of tokens: ' + str(len(tokens)) + '\nNumber of nouns: ' + str(len(all_nouns)))
    return tokens, all_nouns

#---Main---
if len(sys.argv) != 2:
    print("Invalid number of arguments passed in please try again.")
else:
    #open and read file
    with open(sys.argv[1], 'r') as file:
        raw_text = file.read()

    #calculate lexical diversity to two decimals
    tokens = word_tokenize(raw_text)
    diversity_ratio = get_diversity_ratio(tokens)
    print("Lexical diversity: %.2f" % diversity_ratio)

    #prepare word bank for word guessing game
    word_bank = create_word_bank(tokens)
    game_loop(word_bank)
