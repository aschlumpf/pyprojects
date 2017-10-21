'''
A script that determines the best word that can be made given some board state. The given dictionary is small, but larger ones can be used.
'''

scrabbleScores = [ ["a", 1], ["b", 3], ["c", 3], ["d", 2], ["e", 1],
["f", 4], ["g", 2], ["h", 4], ["i", 1], ["j", 8], ["k", 5], ["l", 1],
["m", 3], ["n", 1], ["o", 1], ["p", 3], ["q", 10], ["r", 1], ["s", 1],
["t", 1], ["u", 1], ["v", 4], ["w", 4], ["x", 8], ["y", 4], ["z", 10] ]
from cs115 import filter, map, reduce
import sys
sys.setrecursionlimit(10000)
Dictionary = ["a", "am", "at", "apple", "bat", "bar", "babble", "can", "foo",
"spam", "spammy", "zzyzva"]

def letterScore(letter, scoreList):
    ''' Takes in a letter and a scoreList and returns the letter's value from the given scoreList. '''
    if letter == '':
        return 0
    if letter == scoreList[0][0]:
        return scoreList[0][1]
    return letterScore(letter, scoreList[1:])

def wordScore(S, scoreList):
    ''' Takes in a word and returns its value by recursively calling letterScore to each of the word's letters. '''
    if S == '':
        return 0
    return letterScore(S[0], scoreList) + wordScore(S[1:], scoreList)


def ind(e, L):
    ''' Helper function, takes in a letter and a list or string, returns the index of the first occurrence of that letter  '''
    if L == [] or L == '':
        return 0
    elif e == L[0]:
        return 0
    return 1 + ind(e, L[1:])

def remove(letter, rack):
    '''Removes one occurrence of letter from the rack, by using the ind function to find the letter's index, then slicing the list from 0 to that found index,
    added to the slice of that index + 1 to the end of the list. Assumes rack is a list of letters.'''
    if letter in rack:
        return rack[0:ind(letter, rack)] + rack[ind(letter, rack) + 1:]
    return rack


def is_word_possible(word, rack):
    '''Returns True if word (a string) can be made from letters in the rack,
    False otherwise. Assumes rack is a list of letters. '''

    if word == '':
        return True
    if word[0] in rack:
        return is_word_possible(word[1:], remove(word[0], rack))
    return False


def list_of_words_created(dictionary, rack):
    '''Returns a list of all words in the dictionary that can be made from the rack.'''
    if dictionary == []:
        return []
    if is_word_possible(dictionary[0], rack):
        return [dictionary[0]] + list_of_words_created(dictionary[1:], rack)
    return list_of_words_created(dictionary[1:], rack)

def scoreList(Rack):
    ''' Returns a list of all possible words that can be created from a Rack, accompanied by their value. '''
    if list_of_words_created(Dictionary, Rack) == []:
        return [['', 0]]
    return map(lambda x : [x[0:]] + [wordScore(x, scrabbleScores)], list_of_words_created(Dictionary, Rack))

def greater(x, y):
    '''Helper function, returns whatever list has a higher value at index 1. '''
    if y[1] > x[1]:
        return y[0:]
    return x[0:]

def bestWord(Rack):
    ''' Returns the best possible word that can be created from a Rack, accompanied by its value. '''
    return reduce(greater, scoreList(Rack))

def validInput(inp):
    return len(inp) > 1

if __name__ == '__main__':
    output = []
    while(1):
        print("Welcome to Scrabble Cheater. Find out the best possible word in a rack by successively entering letters. Press 2 when done.")
        inp = ""
        while(inp != '2'):
            inp = input("Enter a letter or 2 to finish: ")
            if (len(inp) > 1 or isinstance(inp, str)):
                print('Please enter a letter.')
            output.append(inp)
        i = 0
        scores = scoreList(output)
        for result in scores:
            print('Result ' + str(i) + ': ' + result[0] + ' with a score of ' + str(result[1]) + '.')
            i += 1
        best = bestWord(output)[0]
        print("The best word possible is \'" + best + '\' with a score of ' + str(wordScore(best, scrabbleScores)) + '.')
        output = []
        cont = input("Would you like to continue? (y/n) ")
        if (cont == "n"):
            break
