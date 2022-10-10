import math
from nltk import word_tokenize
from nltk.corpus import stopwords

stopwords = stopwords.words('english')
num_docs = 17

# gather all the tokens in the data files into the data dictionary
# file0 has data from site 0 and etc
data = {}
temp = ""
for x in range(17):
    string = 'data/site_' + str(x) + '.txt'
    with open(string, 'r') as f:
        temp = f.read().lower()
        temp = temp.replace('\n', ' ')
        data["file{0}".format(x)] = temp

vocab = set()  # set of words


# create tf dictionaries for each document
def create_tf_dict(doc):
    tf_dict = {}
    tokens = word_tokenize(doc)
    tokens = [w for w in tokens if w.isalpha() and w not in stopwords]

    # get term frequencies
    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1

    token_set = set(tokens)
    tf_dict = {t: tokens.count(t) for t in token_set}

    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)

    return tf_dict


# create tf for each site data
tf_site0 = create_tf_dict(data.get('file0'))
tf_site1 = create_tf_dict(data.get('file1'))
tf_site2 = create_tf_dict(data.get('file2'))
tf_site3 = create_tf_dict(data.get('file3'))
tf_site4 = create_tf_dict(data.get('file4'))
tf_site5 = create_tf_dict(data.get('file5'))
tf_site6 = create_tf_dict(data.get('file6'))
tf_site7 = create_tf_dict(data.get('file7'))
tf_site8 = create_tf_dict(data.get('file8'))
tf_site9 = create_tf_dict(data.get('file9'))
tf_site10 = create_tf_dict(data.get('file10'))
tf_site11 = create_tf_dict(data.get('file11'))
tf_site12 = create_tf_dict(data.get('file12'))
tf_site13 = create_tf_dict(data.get('file13'))
tf_site14 = create_tf_dict(data.get('file14'))
tf_site15 = create_tf_dict(data.get('file15'))
tf_site16 = create_tf_dict(data.get('file16'))

# add to vocab
vocab = set(tf_site0.keys())
vocab = vocab.union(set(tf_site1.keys()))
vocab = vocab.union(set(tf_site2.keys()))
vocab = vocab.union(set(tf_site3.keys()))
vocab = vocab.union(set(tf_site4.keys()))
vocab = vocab.union(set(tf_site5.keys()))
vocab = vocab.union(set(tf_site6.keys()))
vocab = vocab.union(set(tf_site7.keys()))
vocab = vocab.union(set(tf_site8.keys()))
vocab = vocab.union(set(tf_site9.keys()))
vocab = vocab.union(set(tf_site10.keys()))
vocab = vocab.union(set(tf_site11.keys()))
vocab = vocab.union(set(tf_site12.keys()))
vocab = vocab.union(set(tf_site13.keys()))
vocab = vocab.union(set(tf_site14.keys()))
vocab = vocab.union(set(tf_site15.keys()))
vocab = vocab.union(set(tf_site16.keys()))

idf_dict = {}

vocab_by_topic = [tf_site0.keys(), tf_site1.keys(), tf_site2.keys(), tf_site3.keys(), tf_site4.keys(), tf_site5.keys(),
                  tf_site6.keys(), tf_site7.keys(), tf_site8.keys(), tf_site9.keys(), tf_site10.keys(),
                  tf_site11.keys(),
                  tf_site12.keys(), tf_site13.keys(), tf_site14.keys(), tf_site15.keys(), tf_site16.keys()]

# create idf dictionary
for term in vocab:
    temp = ['x' for voc in vocab_by_topic if term in voc]
    idf_dict[term] = math.log((1 + num_docs) / (1 + len(temp)))


# create tf-idf dictionary for each site data
def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t]

    return tf_idf


tf_idf_site0 = create_tfidf(tf_site0, idf_dict)
tf_idf_site1 = create_tfidf(tf_site1, idf_dict)
tf_idf_site2 = create_tfidf(tf_site2, idf_dict)
tf_idf_site3 = create_tfidf(tf_site3, idf_dict)
tf_idf_site4 = create_tfidf(tf_site4, idf_dict)
tf_idf_site5 = create_tfidf(tf_site5, idf_dict)
tf_idf_site6 = create_tfidf(tf_site6, idf_dict)
tf_idf_site7 = create_tfidf(tf_site7, idf_dict)
tf_idf_site8 = create_tfidf(tf_site8, idf_dict)
tf_idf_site9 = create_tfidf(tf_site9, idf_dict)
tf_idf_site10 = create_tfidf(tf_site10, idf_dict)
tf_idf_site11 = create_tfidf(tf_site11, idf_dict)
tf_idf_site12 = create_tfidf(tf_site12, idf_dict)
tf_idf_site13 = create_tfidf(tf_site13, idf_dict)
tf_idf_site14 = create_tfidf(tf_site14, idf_dict)
tf_idf_site15 = create_tfidf(tf_site15, idf_dict)
tf_idf_site16 = create_tfidf(tf_site16, idf_dict)

# put top words from each into list
topWords = []
doc_term_weights = sorted(tf_idf_site0.keys(), key=lambda x: -tf_idf_site0[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site2.keys(), key=lambda x: -tf_idf_site2[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site3.keys(), key=lambda x: -tf_idf_site3[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site4.keys(), key=lambda x: -tf_idf_site4[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site5.keys(), key=lambda x: -tf_idf_site5[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site6.keys(), key=lambda x: -tf_idf_site6[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site7.keys(), key=lambda x: -tf_idf_site7[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site8.keys(), key=lambda x: -tf_idf_site8[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site9.keys(), key=lambda x: -tf_idf_site9[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site10.keys(), key=lambda x: -tf_idf_site10[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site11.keys(), key=lambda x: -tf_idf_site11[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site12.keys(), key=lambda x: -tf_idf_site12[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site13.keys(), key=lambda x: -tf_idf_site13[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site14.keys(), key=lambda x: -tf_idf_site14[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site15.keys(), key=lambda x: -tf_idf_site15[x])
topWords.extend(doc_term_weights[:3])
doc_term_weights = sorted(tf_idf_site16.keys(), key=lambda x: -tf_idf_site16[x])
topWords.extend(doc_term_weights[:3])

print(topWords)
