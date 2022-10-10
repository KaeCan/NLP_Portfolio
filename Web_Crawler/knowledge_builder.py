import pickle
from os import listdir
from os.path import isfile, join

#retrieve a list of all sites previously scraped
sites = [file for file in listdir('data\\') if isfile(join('data\\', file))]

#{term: list of sentences relating to term}
knowledge_base = {}

print('Choose 10 terms to search for:')

for x in range(10):
    #retrieve user input
    term = input("Type in a term: ")

    #compile all sentences that have the specified term into a list
    cumulative_list = []
    for site in sites:
        with open('data\\' + site, 'r') as f:
            lines = f.read().splitlines()
            trunc_lines = lines[10:]    #ignore the beginning of each file, usually filled with junk info

            has_term_list = [line for line in trunc_lines if term in line]  #extract all sentences that have the term in it

            cumulative_list += has_term_list

    #add term entry
    knowledge_base[term] = cumulative_list

    print(str(knowledge_base[term]) + '\n\n\n')

#pickle dictionary for future use
pickle.dump(knowledge_base, open('knowledge_base.p', 'wb'))
