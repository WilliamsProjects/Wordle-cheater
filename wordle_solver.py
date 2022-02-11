import numpy as np
import pandas as pd


def wordle_solver(black_letters, yellow_letters, green_letters):
    '''
    Given a list of black letters and yellow/green letters with their respective positions, this function
    finds all possible Wordle words (i.e. 5 letter words).

    Inputs:
    black_letters: list of strings, All letters which are either not in the Wordle word, or are not in the word
    as many times as guessed for that guess.

    yellow_letters: dictionary, All letters which are placed in the wrong place in the word and the incorrect position(s)
    they were placed

    green_letters: dictionary, All letters which are placed in the right place in the word and the correct position(s)
    they were placed

    Outputs:
    final_words: list of strings, All possible words given the input black, green and yellow letters and their positions.
    '''


    #Reading in all 5 letter words
    words = pd.read_csv('words.csv')
    word_list = list(words.dictionary)

    #finding letters in both black and in yellow and/or green
    yellow = list(yellow_letters.keys())
    green = list(green_letters.keys())
    yellow.extend(green_letters)
    union_letters = set(black_letters).intersection(set(yellow))

    #getting letters in both black and in yellow and/or green out of black letters
    
    black_letters = [elem for elem in black_letters if elem not in union_letters]


    #Removing all black letters which aren't also yellow/green letters

    word_list = [elem for elem in word_list if not contains_letter(black_letters,elem)]

    #Getting words with yellow letters in them but not in the same place as the yellow letters were placed

    new_word_list = []

    for word in word_list:
        count = 0
        for key in yellow_letters:
            
            #Only append word to list if the words contains each letter in yellow letters and index(es) where they are 
            #placed is different to the index(es) of those letters in the word
            if contains_letter(key,word) and set(get_letter_index(key,word)) != set(yellow_letters[key]):
                count = count + 1

            if count == len(yellow_letters):
                new_word_list.append(word)

    #Getting words where the green letters are in the same position as where the green letters were placed

    final_words = []
    for word in new_word_list:
        count = 0
        for key in green_letters:

            if contains_letter(key,word) and set(get_letter_index(key,word)) == set(green_letters[key]):
                count = count + 1
                
            if count == len(green_letters):    
                final_words.append(word)


    #Removing words where the number of letters which are present in both the black letters and yellow and/or green letters
    #exceeds the max number of allowable letters
    words = final_words.copy()

    if len(union_letters) != 0:
        for letter in union_letters:
            
            #if black letter also in yellow and green, the number of letters allowed for that letter = 
            #number of times letter is present as a yellow letter + number of times letter is present as a green letter

            if letter in yellow_letters.keys() and letter in green_letters.keys():
                num_letters_allowed = len(yellow_letters[letter]) + len(green_letters[letter])

            elif letter in yellow_letters.keys():
                num_letters_allowed = len(yellow_letters[letter])

            else:
                num_letters_allowed = len(green_letters[letter])


        final_words = [elem for elem in final_words if num_letters_in_word(letter,elem) == num_letters_allowed]

    return final_words

def contains_letter(letters,word):
    '''
    Returns whether or not a word contains one or more of a list of letters

    Inputs:
    letters, list of strings: All letters to check are in word

    word: string, the word the check

    Outputs:
    bool, True/False based on whether the word contained any one of the letters

    '''

    for letter in letters:
        if letter in word:
            return True

    
    return False

def get_letter_index(letter,word):
    '''
    Finds the index (or indices) where a letter occurs in a word

    Inputs:
    letter, string: Letter to check in word

    word: string, the word the check

    Outputs:
    indices, list of ints: Index (or indices) where letter occurs in word
    '''

    indices = []

    for i in range(len(word)):
        if letter == word[i]:
            indices.append(i)

    return indices

def num_letters_in_word(letter,word):
    '''
    Finds the number of times a letter occurs in a word

    Inputs:
    letter, string: Letter to check in word

    word: string, the word the check

    Outputs:
    count, int: Number of instances of letter in word
    '''

    count = 0
    for char in word:
        if char == letter:
            count = count + 1

    return count

def wordle_user_io():

    stop = 'stop'
    black_letters = []
    while True:
        black_letter = input(f'\nEnter one new black letter. If you have entered all black letters enter {stop}:  ')

        if black_letter == stop:
            break
        
        black_letters.append(black_letter)


        

    
    yellow_letters = {}

    while True:
        yellow_letter = input(f'\nEnter a yellow letter. If you have entered all yellow letters enter {stop}:  ')
        if yellow_letter == stop:
            break
        yellow_index = int(input(f'\nEnter the position(s) where the you have placed the yellow letter:  '))

        yellow_letters[yellow_letter] = yellow_index
    
    green_letters = {}

    while True:
        green_letter = input(f'\nEnter a green letter. If you have entered all green letters enter {stop}:  ')

        if green_letter == stop:
            break

        green_index = int(input(f'\nEnter the position(s) where the you have placed the green letter:  '))

        green_letters[green_letter] = green_index


    possible_words = wordle_solver(black_letters,yellow_letters,green_letters)

    print(f'The list of possible words is: \n\n {possible_words}')
    


if __name__ == "__main__":
    wordle_user_io()

