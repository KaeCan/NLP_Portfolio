from bs4 import BeautifulSoup
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

#arg: n most important/frequent terms
#lower-case, remove stopwords and punctuation, and use FreqDist
#return a list of the words
#def extract_important_terms(n):

#arg: list of urls
#store texts in individual files in /data
#return nothing
#def scrape_url_text(urls):
    #TODO: get texts from urls

    #before saving as a file, clean up the texts


#-----Main-----
#Topic: Astronomy -> Black Holes
start_url = "https://www.space.com/15421-black-holes-facts-formation-discovery-sdcmp.html"
r = requests.get(start_url)

data = r.text
soup = BeautifulSoup(data)

#get the first n urls
n = 0
url_list = []
for link in soup.find_all('a'):
    n += 1
    link_str = str(link.get('href'))
    if 'black-hole' in link_str or 'black-holes' in link_str:
        if link_str.startswith('/url?q='):
            link_str = link_str[7:]
            print('MOD:', link_str)
        if '&' in link_str:
            i = link_str.find('&')
            link_str = link_str[:i]
        if link_str.startswith('http') and 'google' not in link_str:
            url_list.append(link_str)
            print(link_str)


#scrape texts from urls
#get top n most important terms
#send top 10 terms to some knowledge base (e.g. pickle dictionary, SQL)
