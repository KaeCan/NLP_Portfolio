# NLP_Portfolio
A portfolio for NLP class CS 4395

---
## Overview of NLP

A [document](Overview_of_NLP.pdf) summarizing NLP and my views on it.

---
## Simple Text Processing

This program takes a data sheet with employee information and asks the user to normalize/correct the information as needed. The information is then placed into a dictionary that is finally pickled.

You can see the [code here](https://github.com/KaeCan/NLP_Portfolio/blob/main/Homework1/Homework1_kxc180021.py).

---
## Exploring NLTK

This is a Python notebook documenting my first experience and usage of NLTK. I explain a few basic methods and use cases, and I provide simple explanations and comparisons on common methods.

You can see the [notebook here](https://github.com/KaeCan/NLP_Portfolio/blob/main/Exploring_NLTK.ipynb).

---
## Word Guessing Game

This is a program that was used to explore Python and NLTK features in analyzing text files. First, it extracts text from a large file, in this case an entire chapter from an anatomy textbook. Then, lexical analysis and preprocessing will be performed to prepare words for a word guessing game.

The guessing game is essentially a variation of Hangman, where users guess letters and receive a score dependent on how well they did.

You can see the [code here](https://github.com/KaeCan/NLP_Portfolio/blob/main/Word_Guesser/word_guess_game.py) and the [anatomy text here](https://github.com/KaeCan/NLP_Portfolio/blob/main/Word_Guesser/anat19.txt). I followed this set of [criteria](https://github.com/KaeCan/NLP_Portfolio/blob/main/Word_Guesser/Ch5%20Word%20Guess%20Game.pdf) for grading.

---
## Exploring WordNet

This is a Python notebook documenting my first experience and usage of NLTK's interface with WordNet. I demonstrate a few use cases and how to extract information. You can see the [notebook here](https://github.com/KaeCan/NLP_Portfolio/blob/main/Exploring_WordNet.ipynb).

---
## Language Model from N-grams

This is a program that builds bigram and unigram dictionaries for English, French, and Italian using some training data (here is a [narrative](https://github.com/KaeCan/NLP_Portfolio/blob/main/N-grams/N-grams_Narrative.pdf) on n-grams). For the dictionaries, the keys are the unigram/bigram text, and the value is the count of the unigram/bigram. I use these dictionaries to calculate the probability of a given line of text's likelihood of being a particular language (English, Italian, or French). I used Laplace smoothing for calculations. I outputted my program's guesses for each line of text into this file [here](https://github.com/KaeCan/NLP_Portfolio/blob/main/N-grams/probs_output.txt).

There are two programs: the [first](https://github.com/KaeCan/NLP_Portfolio/blob/main/N-grams/ngrams_builder.py) solely builds and pickles the unigram and bigram dictionaries for each language (time-consuming), and the [second](https://github.com/KaeCan/NLP_Portfolio/blob/main/N-grams/ngrams_probability.py) will unpickle the dictionaries and actually run calculations and output . **If the pickle files are not present already, the first program must be run before the second.**

---
## Web Crawler

This is a basic web-crawling [program](https://github.com/KaeCan/NLP_Portfolio/blob/main/Web_Crawler/corpus_builder.py) that starts at a given URL, and scrapes text off of up to N links to other URLs on that page. The ideal starting URL would be of a topic we want to learn more about. We have chosen the topic of black holes in Astronomy.

We use this scraped data and find the most common terms relating to our topic using TF-IDF (term frequency) (program [here](https://github.com/KaeCan/NLP_Portfolio/blob/main/Web_Crawler/wordExtractor.py), contributed to by my project [partner](https://github.com/RyanBanafshay)). Finally, we built a knowledge base using what we deem as the top 10 most significant terms.

Our knowledge base is a pickled dictionary prepared by associating the terms we've selected with all sentences related to their respective term (program [here](https://github.com/KaeCan/NLP_Portfolio/blob/main/Web_Crawler/knowledge_builder.py)).

In the future, this dictionary will be used in the production of a basic chat bot.

---
## Sentence Syntax Overview

A brief overview with my first experience and opinions on PSG, dependency parsing, and SRL. Click [here](https://github.com/KaeCan/NLP_Portfolio/blob/main/Sentence_Syntax.pdf)
