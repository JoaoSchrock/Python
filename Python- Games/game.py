############################################
# File: game.py
# Author: AJ. Gauld
# Copyright: December 2000
# 
# This file provides an object framework for guessing games
# The framework comprises 3 classes:
# Game 
#	looks after coordination and display of results
# Target 
#	contains the goal to be guessed and provides the 
# 	evaluation mechanism to determine whether the goal 
#	has been guessed yet.
# Guess
#	holds a single guess, The game may hold a list of these 
# 	and the values are submitted to the Target for evaluation.
#
# All of these classes will be overridden to implement any 
# specific gussing game.
############################################

class Game:
   ''' Game class coordinates guessing games

   The Game class is respoinsible for intial display, 
   coordination of the generation of guesses and the 
   display of outcomes of guesses '''
   def __init__(self):
     self.theTarget = self.getTarget()
     self.GuessType = Guess
     self.outcome = 1
     self.guesses = []

   # main function, checks score and stops when done    
   def play(self):
     self.displayStart()
     while (self.outcome): 
       self.guesses.append(self.GuessType())
       self.outcome = self.theTarget.eval(self.guesses[-1])
       self.display(self.outcome)
        
   # needs to be overridden to provide right kind of target
   def getTarget(self):
     return Target()

   #play again, init values and redisplay first 'screen'
   def reStart(self):
     self.__init__()
     self.play()

   # show opening screen - may have instructions etc
   def displayStart(self):
     print """
Abstract class: Game.
You need to create an instance of some specific subclass!"""

   # show appropriate display depending on outcome of last guess
   def display(self, outcome):
     if outcome == 0:
       self.outcome = 0

# Guess class gets value(s) from user, presents an object for evaluation
class Guess:
  'Guess holds a value for evaluation by the Target'
  def __init__(self):
     self.theValue = raw_input("Type something: ")

  def value(self):
     return self.theValue

# Target generates the object to be matched. Checks if a guess matches
class Target:
  ''' Target class generates an object to be guessed (the goal) and
evaluates guesses against that goal '''

  def __init__(self):
    self.goal = self.setGoal()

  def setGoal(self):
    return 0

  def getGoal(self):
    return self.goal

  def eval(self, aGuess):
    return 0

##############################################################
############### Test Game #############
    
# simple guess the number game demos framework
class NumberGame(Game):
  def __init__(self):
    Game.__init__(self)
    self.successMsg = "Well done, you got it after %d %s."
    self.guessString = 'guess'
    self.theTarget = self.getTarget()
    self.GuessType = NumberGuess
        
  def displayStart(self):
    print ("\n\nGuess a number between 1 and 100\n")

  def getTarget(self):
    return NumberTarget()

  def display(self,outcome):
    Game.display(self, outcome)
    if len(self.guesses) > 1:
      self.guessString = "guesses"
    if outcome == 0:
      print self.successMsg % (len(self.guesses),
                               self.guessString)
    elif outcome < 0:
      print "Guess higher"
    else:
      print "Guess lower"

# Get a number
class NumberGuess(Guess):
   def __init__(self):
      self.theValue = input("Type a number(1-100) : ")
        
# Generate random number between 1 and 100, compare to guesses
class NumberTarget(Target):
   def setGoal(self):
     import whrandom
     return int(whrandom.random() * 100)
    
   def eval(self, aGuess):
     if self.goal == aGuess.value():
       return 0
     elif self.goal > aGuess.value():
       return -1
     else:
       return 1

#########################################################
# Create a sample game and run it.
if __name__ == "__main__":
    w = NumberGame()
    w.play()
    w.reStart()
    

