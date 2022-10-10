from bs4 import BeautifulSoup
import urllib.request
import re
import requests
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist

#helper to see if the text on a page is visible to the user
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

#arg: list of urls
#store texts in individual files in \data
#return nothing
def scrape_url_text(urls):

    #create directory to store site texts
    data_folder = 'data\\'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    n = 0
    for url in urls:
        try:
            #retrieve all visible text from url
            html = urllib.request.urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            data = soup.findAll(text=True)
            result = filter(visible, data)
            temp_list = list(result)        # list from filter
            temp_str = ' '.join(temp_list)

            #store text in respective file
            file = 'data\site_' + str(n) + '.txt'
            with open(file, 'w+') as f:
                #one sentence per line
                sents = sent_tokenize(' '.join(temp_str.split()))    #tokenize sentences from website while removing newlines and tabs
                for sent in sents:
                    f.write(sent + '\n')
            n += 1
        except:
            print('could not retrieve url: ' + url)

#-----Main-----
#Topic: Astronomy -> Black Holes
start_url = "https://www.space.com/15421-black-holes-facts-formation-discovery-sdcmp.html"
r = requests.get(start_url)

data = r.text
soup = BeautifulSoup(data, 'html.parser')

#get the first n urls
n = 20
url_list = []
for link in soup.find_all('a'):
    link_str = str(link.get('href'))
    #narrow down our search with target keywords and ignoring unwanted urls
    if 'black-hole' in link_str or 'black-holes' in link_str:
        if link_str.startswith('/url?q='):  #adjust url
            link_str = link_str[7:]
            print('MOD:', link_str)
        if '&' in link_str:                 #adjust url
            i = link_str.find('&')
            link_str = link_str[:i]
        #ignore urls
        if link_str.startswith('http') and ('google' not in link_str and 'facebook' not in link_str and 'pinterest' not in link_str and 'twitter' not in link_str):
            n -= 1
            url_list.append(link_str)
            print(link_str)
    if n == 0:
        break

#scrape texts from urls
scrape_url_text(url_list)
