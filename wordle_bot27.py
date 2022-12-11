import wordle_solving_algorithm27
import ast
import json


wordle_solving_algorithm27.createFiles()

def getFirstGuess():
    """ reads first round entropy file and gets best guess by sorting """

    # get best guess for first round from entropy map
    entropyMapFile = open("entropyMap.txt","r")
    line = entropyMapFile.readline()
    entropyMapFile.close()
    eMap = dict(ast.literal_eval(line))
    # sort dictionary
    eMap = dict(sorted(eMap.items(), key=lambda item: item[1]))
    guessList = list(eMap.keys())
    guessList.reverse()

    # return highest entropy guess 
    return guessList[0]


def playRound(wordBank, answer, secondGuessMap, firstGuess):

    ''' simulates a single game of wordle and returns a int from 1-6 if the word is guessed and -1 if it loses

    returns amount of tries it took and current second guess map
    '''

    # get pre-read first guess
    guess = firstGuess
    tries = 0
    # loop until a answer has been returned 
    while True:
        # get result of guess 
        result = wordle_solving_algorithm27.getColors(guess, answer)
        tries += 1
        # if correct answer return amount of tries and the second guess map
        if result == 'ggggg':
            return tries, secondGuessMap
        else:
            
            # trim the bank 
            wordBank = wordle_solving_algorithm27.trimWordBank(wordBank, guess, result)

            # if this result has been done already in first round use guess from map
            if result in secondGuessMap.keys() and tries == 1:
                guess = secondGuessMap[result]

            # if it hasnt been done calculate next guess and add to file
            elif result not in secondGuessMap and tries == 1:
                guess = wordle_solving_algorithm27.getNextGuess(wordBank)
                secondGuessMap[result] = guess

            # if its round 2+ just calculate next guess
            else:
                guess = wordle_solving_algorithm27.getNextGuess(wordBank)


def runBot(firstGuess):
    
    # keeps track of amount of tries a round took
    triesList = []
    fails = 0
    wordBank = wordle_solving_algorithm27.getWordSet()
    secondGuessMap = {}

    # amount of games currently possible in wordle 
    rounds = 2315
    count = 0
    while count < rounds:

        # get what answer this game will use 
        answer = wordBank[count]

        # play a round. gets updated second guess map returned 
        print('current game: ',count+1,'/',rounds, ', answer: ',answer)
        tries, secondGuessMap = playRound(wordBank, answer, secondGuessMap, firstGuess)
        print("it took",tries,'tries to guess',answer, '. first guess: ', firstGuess)
        
        # add a fail if a round takes more than 6 tries 
        if tries > 6:
            fails += 1
        else:
            triesList.append(tries)

        # track what round we are on 
        count += 1  

        # get average tires so far 
        sumOfTries = sum(triesList)
        aveTries = round(sumOfTries / len(triesList), 2)
        print('current average: ',aveTries) 
        print()

    # print final result 
    print('average guesses: ',aveTries,' , fails: ', fails)

    return {firstGuess:aveTries}


def getBestFirst():

    # get best guess for first round from entropy map
    entropyMapFile = open("entropyMap.txt","r")
    line = entropyMapFile.readline()
    entropyMapFile.close()
    eMap = dict(ast.literal_eval(line))
    # sort dictionary
    eMap = dict(sorted(eMap.items(), key=lambda item: item[1]))
    guessList = list(eMap.keys())
    guessList.reverse()
    guessList = guessList[:10]

    bestOptions = []
    for guess in guessList:
        bestOptions.append(runBot(guess))

    print(bestOptions)

runBot("salet")
# [{'tares': 3.66}, {'lares': 3.68}, {'rales': 3.68}, {'tales': 3.64}, {'salet': 3.64}, {'arles': 3.68}, {'rates': 3.67}, {'tears': 3.65}, {'reals': 3.68}, {'tores': 3.65}]