import wordle_solving_algorithm27
import tkinter as tk



wordBank = wordle_solving_algorithm27.getWordSet()

window = tk.Tk()
window.title('wordle solver')
window.geometry('620x200')


# add functional widgets 
guessChoice = tk.Entry(window, width=10)
resultBox = tk.Entry(window, width = 10)
topGuessesBox = tk.Text(window, height = 3, width = 50)
topGuessesBox.insert(tk.END, "1.salet 2.tales 3.tears 4.rates 5.tores\n")
possibleOptionsLeft = tk.Text(window, height = 1 ,width = 10)
possibleOptionsLeft.insert(tk.END, len(wordBank))

# create label widgets 
guessChoiceLabel = tk.Label(window, text = "enter your guess below")
resultBoxLabel = tk.Label(window, text = "green = 'g', yellow = 'y', grey = 'x'\n enter results below in format xggyy")
bestGuessesLabel = tk.Label(window, text = "best guesses")
numOptionsLabel = tk.Label(window, text = "  number of possible answers left")


def getNextGuess(wordBank):
    ''' returns 5 element list of best guesses in order '''
    eMap = wordle_solving_algorithm27.getGuessEntropySet(wordBank)
    eMap2 = wordle_solving_algorithm27.applyCommonWordModifier(eMap)

    eMap2 = dict(sorted(eMap2.items(), key=lambda item: item[1]))
    
    # get guesses into list and reverse it
    guessList = list(eMap2.keys())
    guessList.reverse()

    # return highest entropy guess 
    return guessList[:5]


def reset():
    ''' rests window '''
    global wordBank
    # clear entry boxes 
    guessChoice.delete(0 , tk.END)
    resultBox.delete(0 , tk.END)
    topGuessesBox.delete(1.0, tk.END)
    topGuessesBox.insert(tk.END, "1.salet 2.tales 3.tears 4.rates 5.tores\n")
    possibleOptionsLeft.delete(1.0, tk.END)
    # reset word bank and box for num of options left
    wordBank = wordle_solving_algorithm27.getWordSet()
    possibleOptionsLeft.insert(tk.END, len(wordBank))


def calcButton():
    ''' takes in input, either gives calculation or prints error output.'''

    global wordBank

    # collect guess and result entries 
    guess = guessChoice.get()
    result = resultBox.get()

    # clear result and choice entry boxes 
    guessChoice.delete(0 , tk.END)
    resultBox.delete(0 , tk.END)
    
    # check if inputs are valid and do not continue if not.
    tmp = ''
    currentString = topGuessesBox.get(1.0, tk.END)
    for i in currentString:
        if i != '\n':
            tmp+=i
        else:
            tmp+='\n'
            break
    currentString=tmp
    valid = True
    for i in result:
        if i!='g' and i!='y' and i!='x':
            topGuessesBox.delete(1.0, tk.END)
            topGuessesBox.insert(tk.END, currentString +"invalid result characters.\nfollow format above result box\n\n")
            guessChoice.delete(0 , tk.END)
            resultBox.delete(0 , tk.END)
            valid = False
            break 
    if len(result) != 5:
        topGuessesBox.delete(0.0, tk.END)
        topGuessesBox.insert(tk.END, currentString + "result must be 5 letters\n\n")
        valid = False
    if guess not in wordBank:
        topGuessesBox.delete(0.0, tk.END)
        topGuessesBox.insert(tk.END, currentString +"guess is not possible\n\n")
        valid = False

    if valid:
        topGuessesBox.delete(1.0, tk.END)
        # delete number of Options left
        possibleOptionsLeft.delete(1.0, tk.END)
        # get top guesses  
        wordBank = wordle_solving_algorithm27.trimWordBank(wordBank, guess, result)
        bestOptions = getNextGuess(wordBank)
        #put top guesses into options box
        for i in range(len(bestOptions)):
            boxString = str(i+1)+'.'+bestOptions[i]+' '
            topGuessesBox.insert(tk.END, boxString)
        topGuessesBox.insert(tk.END, '\n')
        # put possible options left into box
        possibleOptionsLeft.delete(1.0, tk.END)
        possibleOptionsLeft.insert(tk.END, len(wordBank))

        # check for incorrect result entry
        if len(wordBank)==0:
            topGuessesBox.insert(tk.END, 'a result has been entered incorrectly.\nreset and try again.')

# create buttons 

calculateButton = tk.Button(window, text='calculate guess', command = calcButton)
resetButton = tk.Button(window, text='reset', command = reset)
exitButton = tk.Button(window, text='exit', command = window.destroy)

# label widgets 
guessChoiceLabel.grid(row=0, column=0)
resultBoxLabel.grid(row=0, column=1)
bestGuessesLabel.grid(row=2, column=0)
numOptionsLabel.grid(row=2, column=1)

# functional widgets
guessChoice.grid(row=1, column=0)
resultBox.grid(row=1, column =1)
topGuessesBox.grid(row=3, column= 0)
possibleOptionsLeft.grid(row= 3, column=1)
calculateButton.grid(row=4, column=0)
exitButton.grid(row=6, column=1)
resetButton.grid(row=6, column=0)


# run main loop
window.mainloop()




