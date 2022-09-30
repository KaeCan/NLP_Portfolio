import nltk
import pickle
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

def process_file(file):

    with open(file, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    f.close()

    unigrams = word_tokenize(raw_text)
    bigrams = list(ngrams(unigrams, 2))

    #dictionaries
    unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}

    #tuple
    return bigram_dict, unigram_dict

#-----Main-----
print('processing English..')
eng_bigrams, eng_unigrams = process_file('LangId.train.English')
print('processing Italian..')
ita_bigrams, ita_unigrams = process_file('LangId.train.Italian')
print('processing French..')
fre_bigrams, fre_unigrams = process_file('LangId.train.French')

print('pickling..')
pickle.dump(eng_bigrams, open('eng_bigrams.p', 'wb'))
pickle.dump(eng_unigrams, open('eng_unigrams.p', 'wb'))
pickle.dump(ita_bigrams, open('ita_bigrams.p', 'wb'))
pickle.dump(ita_unigrams, open('ita_unigrams.p', 'wb'))
pickle.dump(fre_bigrams, open('fre_bigrams.p', 'wb'))
pickle.dump(fre_unigrams, open('fre_unigrams.p', 'wb'))
print('done')
