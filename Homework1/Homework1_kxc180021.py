import sys
import re
import pickle

class Person:
    def __init__(self, first, last, mi, id, phone):
        self.first = first
        self.last = last
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print('Employee id: ' + self.id + '\n\t' + self.first + ' ' + self.mi + ' ' + self.last + '\n\t' + self.phone + '\n')


#returns the first letter as uppercase and the rest as lowercase
def fix_name(name):
    return name.capitalize()


#returns a capital initial, or an 'X' if no middle initial
def fix_mi(mi):
    if not mi:
        return 'X'
    else:
        return mi.capitalize()


#forces a user to enter a valid id if currently invalid
def fix_id(id):
    if re.search("[a-zA-Z][a-zA-Z]\d\d\d\d", id) and len(id) == 6:
        return id
    else:
        id = input('ID invalid: ' + id + '\nID is two letters followed by 4 digits\nPlease enter a valid id: ')
        return fix_id(id)


#forces a user to enter a valid phone number if currently invalid
def fix_phonenum(num):
    if re.search("\d\d\d-\d\d\d-\d\d\d\d", num) and len(num) == 12:
        return num
    else:
        num = input('Phone ' + num + ' is invalid\nEnter phone number in form 123-456-7890\nEnter phone number: ')
        return fix_phonenum(num)


#checks if a key is already in a dictionary
def dupe_key(dict, key):
    if key in dict.keys():
        print('Error: could not input ID ' + key + ' into dictionary.')
        return True
    return False


#args: data to be processed (list)
#return: entried people (dict)
#processes data from file and creates Person objects out of them
def process(in_file):
    people = {} #{ID : person (obj)}
    data = []
    #ignore first line in file
    for line in in_file[1:]:
        data.append(line)

    #split fields on commas
    for line in data:
        fields = line.split(',')

        #last,first,mi,id,num
        first = fix_name(fields[1])
        last = fix_name(fields[0])
        mi = fix_mi(fields[2])
        id = fix_id(fields[3])
        phone_num = fix_phonenum(fields[4])

        #we do not create a new dict entry for duplicate IDs
        if not dupe_key(people, id):
            person = Person(first,last,mi,id,phone_num)
            people.update({id : person})

    return people


#-----main-----
#check for included file path for data input
if len(sys.argv) != 2:
    print("Invalid number of arguments passed in, please try again.")
else:
    #read in and close data file
    with open(sys.argv[1], 'r') as file:
        data = file.readlines()

    #place all people from data input into 'people' dict
    people = process(data)

    #save pickle file
    pickle.dump(people, open('people.p', 'wb'))

    #unpickle file
    unpickled_people = pickle.load(open('people.p', 'rb'))

    #print employees to check we have successfully unpickled
    print('Employee list:\n')
    for person in unpickled_people:
        unpickled_people[person].display()
