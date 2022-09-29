import nltk
import pickle
import math
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

def compute_prob(text, unigram_dict, bigram_dict, N, V):
    #N: number of words from the data
    #V: number of unique words from the data

    #create ngrams from our line of text
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    #laplace smoothing
    p_lapace = 1

    #bigram probability = (bigram count + 1) / (unigram count of first word in bigram + total vocabulary size)

    #todo: compute probability
    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0

        p_laplace = p_laplace * ((n+1)/(d+V))

    print('Probability with laplace smoothing is %.5f' % p_laplace)
    return p_laplace

#-----Main-----
try:
    #unpickle files
    eng_bigrams = pickle.load(open('eng_bigrams.p', 'rb'))
    eng_unigrams = pickle.load(open('eng_unigrams.p', 'rb'))
    ita_bigrams = pickle.load(open('ita_bigrams.p', 'rb'))
    ita_unigrams = pickle.load(open('ita_unigrams.p', 'rb'))
    fre_bigrams = pickle.load(open('fre_bigrams.p', 'rb'))
    fre_unigrams = pickle.load(open('fre_unigrams.p', 'rb'))
except:
    print('There was a problem loading in the pickled files.')
else:
    try:
        #get test texts
        with open('LangId.test', 'r', encoding='utf-8') as file:
            #do not include newline
            raw_test = file.read().splitlines()
    except:
        print('Could not open \'LangId.test\'.')
    else:
        #output file for continuous writing
        outf = open('probabilities.txt', 'a')

        ##todo: compute probs for each line
        for line in raw_test:
            #eng_prob = compute_prob(line, eng_bigrams, eng_unigrams, len(unigrams), len(line) )

        outf.close()
