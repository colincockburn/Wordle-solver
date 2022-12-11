import json
import ast
import math
import os.path


def writeResultMap():
    ''' dont wanna document this. already have the list so who cares'''

    wordBank = getWordSet()

    resultMapFile = open('resultmap.txt', 'w')
    count = 0
    for guess in wordBank:
        guessPossibilityMap = {}
        for answer in wordBank:
            result = getColors(guess, answer)
            guessPossibilityMap[answer] = result

        parentList = [guess,guessPossibilityMap]
        resultMapFile.write(json.dumps(parentList))
        resultMapFile.write('\n')

        count+=1
        if count%5 == 0:
            print(count, '/', len(getWordSet()))


def writeFirstRoundEntropy():

    # get wordBank and the possibilities of each word being an asnwer 
    wordBank = getWordSet()
    multiplierMap = getMultiplierMap()

    # create the file if not present 
    if not os.path.isfile("entropyMap.txt"):
        eFile = open('entropyMap.txt','w')
        eFile.close()

    # get unfinished dictionary from file or make a empty one
    eFile = open('entropyMap.txt','r')
    line = eFile.readline()
    eFile.close()
    if len(line) != 0:
        iMap = dict(ast.literal_eval(line))
    else: iMap = {}

    # get progress so far also print it
    progress = len(list(iMap.keys()))
    print(progress,"/", len(getWordSet()))

    # get a wordbank containing what words we need left 
    leftOfWordBank = wordBank[progress:]

    # open and read result file untill we reach the first word in the shortened wordBank
    # line of form['cigar',{cigar:'ggggg', 'rebut':yxxxx ........}]
    resultFile = open('resultmap.txt','r')
    lineList = (ast.literal_eval(resultFile.readline()))
    resultGuess = lineList[0]
    while resultGuess != leftOfWordBank[0]:
        lineList = (ast.literal_eval(resultFile.readline()))
        resultGuess = lineList[0]

    # add every guess to iMap with its average entropy as its value
    for guess in leftOfWordBank:
        # get map of every result for this guess
        resultMap = lineList[1]

        # get average information of this guess. the function used will likly be udated in the future. date: 2022-04-12
        average = getAveInformation(wordBank,resultMap, multiplierMap)
        iMap[guess] = round(average, 3)

        # open and close each loop so it overwrites the file from last loop
        eFile = open("entropyMap.txt", "w")
        # write the map to file 
        eFile.write(json.dumps(iMap))
        eFile.close()

        # validate user of progress 
        progress += 1
        if (progress%1 == 0):
            print(progress,"/",len(getWordSet()))

        # read the next line for the next loop
        lineList = (ast.literal_eval(resultFile.readline()))


def createFiles():
    ''' creates all neccesary files for effeciency purposes if the do not exist in current directory.'''

    # result map
    if not os.path.isfile('resultmap.txt'):
        print("loading every possible result for every possible guess")
        writeResultMap()

    # get average entropy map if no map
    if not os.path.isfile("entropyMap.txt"):
        print("loading how much information each first guess will give on average. this will take a few minutes.")
        writeFirstRoundEntropy()

    else:
        # check if it exits but not finished 
        file = open('entropyMap.txt','r')
        line = file.readline()
        eMap = dict(ast.literal_eval(line))

        if (len(list(eMap.keys())) != len(getWordSet())):
            print("loading how much information each first guess will give on average. this can take around an hour.")
            writeFirstRoundEntropy()

    
    # create commonWord+.txt if it does not exist 
    if not os.path.isfile("commonWords+.txt"):
        print('loading rest of word bank onto provided common word file.')
        writeCommonWords()


def getWordSet():
    ''' gets word set from txt file'''
    wordSetFile = open('word_set.txt','r')
    setLine = wordSetFile.readline()
    wordSet = list(ast.literal_eval(setLine))
    return wordSet


def getFreqMap(list1):
    ''' returns a dictionary containg frequncies for list paremeter'''
    freq = {}
    for elem in list1:
        if elem not in freq:
            freq[elem] = 1
        else:
            freq[elem] += 1
    return freq


def getColorFreq(guess ,result):
    ''' returns frequency of what letters recive a color in result'''

    colorLetterFreq = {}
    for i in range(5):
        if result[i] != 'x':
            ch = guess[i]
            if ch not in colorLetterFreq:
                colorLetterFreq[ch] = 1
            else:
                colorLetterFreq[ch] += 1
    return colorLetterFreq       


def trimWordBank(wordBank, guess, result):
    ''' takes wordbank, guess, and result as parameters. returns a trimmed wordbank containing the only possible words left'''

    wordBank = set(wordBank)
    toBeRemoved = set({})
    colorFreq = getColorFreq(guess, result)

    for word in wordBank:

        wordFreq = getFreqMap(word)

        for i in range(5):
            
            ch = guess[i]
            # Check for green letters
            if result[i] == 'g':
                # remove word if letter at current index doesnt match guess 
                if word[i] != ch:
                    toBeRemoved.add(word)

            elif result[i] == 'y':
                if ch not in word:
                    toBeRemoved.add(word)
                # remove word if it has this letter at this index
                if ch == word[i]:
                    toBeRemoved.add(word)
            
            elif result[i] == 'x':
                # remove word if it has this letter at this index
                if word[i] == ch:
                    toBeRemoved.add(word)

                # remove word if it has this letter and this letter isnt colored anywhere in guess
                elif ch not in list(colorFreq.keys()) and ch in word:
                    toBeRemoved.add(word)

                # if letter appears somewhere else in word and was guessed too many times
                # we know only words that have this letter as often as it is colored work
                else:
                    # get frequency of letters in current word getting checked
                    if ch in list(wordFreq.keys()) and ch in list(colorFreq.keys()):
                        if wordFreq[ch] != colorFreq[ch]:
                            toBeRemoved.add(word) 
                      
    return list(wordBank.difference(toBeRemoved))


def getColors(guess, answer):
    ''' returns a string of form "ggyxg" representing the colors a guess would get highlighted with for a specific answer'''

    ''' get greens '''
    greenList = []

    for i in range(len(guess)):
        if guess[i] == answer[i]:
            greenList.append(True)
        else:
            greenList.append(False)

    '''get yellows'''

    yellowList = []
    letterFreq = getFreqMap(answer)

    # lower occurence in letterFreq of any letter green in guess
    for i in range(len(guess)):
        if greenList[i] == True:
            letterFreq[guess[i]] -= 1
    
    # fill yellow list 

    for i in range(len(guess)):
        
        if guess[i] in answer and greenList[i]==False and letterFreq[guess[i]] > 0:
            yellowList.append(True)
            letterFreq[guess[i]] -= 1
        else:
            yellowList.append(False)

    ''' returns a list of color results for guess in format ggygx'''

    colorString= ''

    for i in range(len(guess)):
        
        if greenList[i] == True:
            colorString+='g'
        elif yellowList[i] == True:
            colorString+='y'
        else:
            colorString+='x'

    return colorString
    

def getAveInformation(wordBank, results, multipliers):
    """ takes wordbank of any size and returns average entropy of given guess. it is assumed that results map given is edited to match wordBank 

    parameters:
    wordBank - ['cigar', 'rebut' .....]
    guess - 'cigar'
    results - {'cigar':'ggggg','rebut':'yxxxx', ......}
    returns: int average information.
    """

    # get result frequency for guess of form {'ggggg':1, xxxxx:2000, .....}
    resultFreq = getFreqMap(list(results.values()))

    # use equation: sum of (information from result X probabilty of result happening)
    total = 0
    for result in list(resultFreq.keys()):

        actualOptions = 0
        for answer in list(results.keys()):
            if results[answer] == result:
                actualOptions += multipliers[answer]

        # p represents the probability of this result happening
        p = actualOptions/len(wordBank)
        # i is basically a nicer looking number.
        i = math.log(1/p,2)
        total += p*i

    return total


def getGuessEntropySet(wordBank):
    ''' returns a unsorted map of each guess and its entropy. used for second round and above as first round takes too long.
    '''

    multipliers = getMultiplierMap()
    # holds all guesses and their average entropy 
    eMap = {}
    for guess in wordBank:
        # results of every answer for every guess. like results.txt
        resultsMap = {}
        for answer in wordBank:
            # get result of this guess for this answer
            result = getColors(guess, answer)
            resultsMap[answer] = result
        # add average information of current guess into emap
        eMap[guess] = getAveInformation(wordBank,resultsMap, multipliers)

    return eMap


def writeCommonWords():

    # get common word list from txt file.
    wordBank = getWordSet()
    commonWords = []
    file = open('commonWords.txt', 'r')
    line = None
    while line != "":
        line = file.readline()
        line = line.rstrip("\n")
        if line in wordBank:
            commonWords.append(line)
    file.close()

    # add any words not in list to end 
    wordBank = getWordSet()
    for word in wordBank:
        if word not in commonWords:
            commonWords.append(word)

    # write new list to file
    newFile = open('commonWords+.txt', 'w')
    for word in commonWords:
        newFile.write(word)
        newFile.write("\n")
    newFile.close()


def sigmoid(x):
    ''' takes a x argument and returns the y value based on a modifed sigmoid function 
    current version: top = aprox 1400, middle = 3500
    '''

    e = math.e
    power = ((1/250)*x - 14)
    y = 1/(1 + math.pow(e,(power)))
    return y


def getMultiplierMap():

    # holds what value each word has in sigmoid function 
    multiplierMap = {}
    # read each line in common words file and get new value
    file = open('commonWords+.txt','r')
    line = file.readline()
    line = line.rstrip("\n")

    # tracks index for function
    x = 0
    while line != '':

        if line == 'grail':
            pass

        # get entropy of current word in common words
        y = sigmoid(x)
        multiplierMap[line] = y
        # get next line for next loop
        line = file.readline()
        line = line.rstrip("\n")
        # change index for function
        x += 1
    return multiplierMap


def applyCommonWordModifier(eMap):
    ''' takes in eMap and returns the same map with values multiplied by their frequency fraction from sigmoid function'''
    
    # holds what value each words entropy is multiplied by
    multiplierMap = getMultiplierMap()

    eMap2 = {}
    for guess in list(eMap.keys()):
        eMap2[guess] = multiplierMap[guess] * eMap[guess]
    
    return eMap2


def getNextGuess(wordBank):

    """ intended for rounds after the first """

    # get unsorted eMap
    eMap = getGuessEntropySet(wordBank)
    eMap2 = applyCommonWordModifier(eMap)
    # sort map lowest to higest entropy
    eMap2 = dict(sorted(eMap2.items(), key=lambda item: item[1]))
    
    # get guesses into list and reverse it
    guessList = list(eMap2.keys())
    guessList.reverse()

    # return highest entropy guess 
    return guessList[0]

