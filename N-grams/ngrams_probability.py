import nltk
import pickle
import math
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

def compute_prob(text, unigram_dict, bigram_dict, V):
    #V: number of unique words from the data

    #create unigrams and bigrams from our line of text
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    #Laplace smoothing
    p_laplace = 1

    #bigram probability = (bigram count + 1) / (unigram count of first word in bigram + total vocabulary size)
    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0

        p_laplace = p_laplace * ((n+1)/(d+V))

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
        outf = open('probs_output.txt', 'w+')

        #get the file with the correct language for each line
        try:
            with open('LangId.sol', 'r', encoding='utf-8') as sol:
                real_langs = sol.read().splitlines()
        except:
            print('Coult not open \'LangId.sol\'.')


        count = 0 #holding line index of LangId.sol
        correct = 0
        print('Incorrectly guessed lines: ')
        #compute probs for each line, compare to LangId.sol and determine correctness
        for line in raw_test:

            prob_list = []

            eng_prob = compute_prob(line, eng_unigrams, eng_bigrams, len(eng_unigrams))
            ita_prob = compute_prob(line, ita_unigrams, ita_bigrams, len(ita_unigrams))
            fre_prob = compute_prob(line, fre_unigrams, fre_bigrams, len(fre_unigrams))

            prob_list.append(eng_prob)
            prob_list.append(ita_prob)
            prob_list.append(fre_prob)

            ##debug
            #print('prob for eng: ', prob_list[0])
            #print('prob for ita: ', prob_list[1])
            #print('prob for fre: ', prob_list[2])

            sol_list = real_langs[count].split() #[0]: line number , [1]: language

            #write down our guess on the language in the output file
            #print out incorrectly guessed line numbers
            index = prob_list.index(max(prob_list))
            match index:
                case 0:
                    outf.write('English\n')
                    if sol_list[1] == 'English':
                        correct += 1
                    else:
                        print(sol_list[0])
                case 1:
                    outf.write('Italian\n')
                    if sol_list[1] == 'Italian':
                        correct += 1
                    else:
                        print(sol_list[0])
                case 2:
                    outf.write('French\n')
                    if sol_list[1] == 'French':
                        correct += 1
                    else:
                        print(sol_list[0])

            count += 1

        print('Total correct: ', correct)
        print('Accuracy: ', correct / len(real_langs))
        outf.close()
