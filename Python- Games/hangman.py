######################
# File: Hangman.py
# Author:   A.J. Gauld
# Version: 0.1
# Date:    2nd April 2000
######################
# Implements a Hangman game based on the game
# framework from game.py
# A list of words is stored in a text file which is 
# read by the target and a radom word selected.
# The game generates multiple guesses, each with 1 letter.
# The Target.eval() checks whether the latest guess 
# is in the goal. The game displays the word by scanning 
# the list of guessed letters and comparing to the target.
######################

import game, whrandom, string

########### GAME ##########
class Hangman(game.Game):
    wordfile = 'hangman.words'
    def __init__(self):
        game.Game.__init__(self)
        self.GuessType = hmGuess
        self.outcome = 6    # use outcome to count lives
    
    # Just display the initial word to guess and the lives
    def displayStart(self):
        self.display(6)

    def getTarget(self):
        return hmTarget()
    
    # helper function constructs result word from guesses
    def getResult(self):
        theWord = ''
        guessed = []
        
	# generate list of letters guessed so far
        if self.guesses:
           for g in self.guesses:
              guessed.append(g.value())
        
	# Now check target against guessed letters
        for c in self.theTarget.getGoal():
           if (c in guessed):
             theWord =  theWord + c
           else:
             theWord = theWord + "_"
        return theWord
    
    def display(self, outcome):
        theWord = self.getResult()
        # sort out singular/plural messages
	if  outcome == 1: lives = 'life'
        else: lives = 'lives'
        
	# check if we're done yet and report result
	if '_' in theWord and  outcome == 0:
           print "Sorry you lose, the word was ", self.theTarget.getGoal()
        elif '_' not in theWord:
           print  "Well done, you got it!"
           import sys;sys.exit()
        else:
           print  "Word to guess: %s\t You have %d %s left" % (theWord, 
	                                                       outcome, 
							       lives)
            
########### GUESS ##########
class hmGuess(game.Guess):
    def __init__(self):
        self.theValue = raw_input("Type a letter:  ")
	
	# if more than 1 just use the first
        if len(self.theValue) > 1: self.theValue = self.theValue[0]
        # if not a string give them a final chance!
	if self.theValue not in string.letters:
            self.theValue = raw_input("It must be a letter! ")

########## TARGET ##########
# Track the lives here and just decrement the value if 
# the guess is not in the target. We generate the random word
# from the word file stored in the Hangman class variable.
# ##########################
class hmTarget(game.Target):
    def __init__(self):
        self.lives = 6
        try:
            wrdFile = open(Hangman.wordfile, "r")
            wordList =  wrdFile.readlines()
        except IOError:
	    # use a temporary wordlist
            wordList = ['now\n',
	                'for\n',
			'something\n',
			'completely\n',
			'different\n']
			
        # minus 1 to account for len being longer than highest index
        index = int( whrandom.random() * (len(wordList)-1))
        self.goal = wordList[index][:-1] # lose \n from end

    # eval returns the number of lives left    
    def eval(self, aGuess):
        if aGuess.value() not in self.goal:
            self.lives  = self.lives - 1
        return  self.lives
    
######### DO IT ############
if __name__ == "__main__":
    Hangman().play()
    
