################################
# File: hmgui.py
# Author: A.J. Gauld
# Copyright: 24-Feb-2001
#
#################################
# Implements a GUI version of the game hangman
# It uses the hangman module which is in turn 
# based on the game modules object framework.
# In addition it used a set of 6 gif files to 
# represent the scaffold plus the hangman.words 
# file from the hangmanmodule. Thus, in addition 
# to vanilla python with Tkinter you need:
# game.py. hangman.py, hmgui.py and
# hangman.words, hm0.gif, hm1.gif, ..., hm6.gif
##################################

from Tkinter import *
import hangman,string

# The keys as we want to display them in the GUI.
keys = [ ['A','B','C','D'],
         ['E','F','G','H'],
         ['I','J','K','L'],
         ['M','N','O','P'],
         ['Q','R','S','T'],
         ['U','V','W','X'],
             ['Y','Z'] ]

# Guess takes a parameter corresponding to the key clicked
class hmGUIGuess( hangman.hmGuess):
	def __init__(self, ch):
	    self.theValue = string.lower(ch)

# control of the game just passes to Tkinter
# most work is in building the GUI and displaying outcome
# we build the GUI in the displayStart method
# The application inherits from both the Hangman game 
# and the Tkinter Frame classes
class hmGUI(Frame, hangman.Hangman):
	def __init__(self, parent=0):
	    # call the parent constructors
	    hangman.Hangman.__init__(self)
	    Frame.__init__(self,parent)
	    self.imgpath = '' # put gif files elsewhere if we want
	    self.firstImg=self.imgpath+'hm6.gif'
	    self.letters = {}
	    self.master.title('Hangman') # set the app title bar
	    self.displayStart()

	def display(self, chr):
	    lossmsg = 'You lost! The word was\n\t%s'
	    playmsg = 'Your target is:\n\t %s'
	    successmsg = 'Well done, you guessed it!'
	    
	    # mark letter as used
	    self.letters[chr].config(state=DISABLED)
	    
	    # create a guess
	    self.guesses.append(hmGUIGuess(chr))
	    
	    # decrease lives if wrong
	    self.lives = self.theTarget.eval(self.guesses[-1])
	    txt = self.getResult()
	    if self.lives > 0: 
		if '_' not in txt:
			txt = successmsg
		else: txt = playmsg % txt
	    else:
		txt = lossmsg % self.theTarget.getGoal()
	    self.status.configure(text=txt) 
	    
	    #now update image
	    thefile = self.imgpath + 'hm' + str(self.lives) + '.gif'
	    self.theImg.configure(file=thefile)

	def getTarget(self):
	    return hangman.hmTarget()
	
	# override the Game.play method to call the Tkinter mainloop
	def play(self):
		self.mainloop()

	# event handler for Quit button
	def quit(self):
	    import sys
	    sys.exit()
	    
	# event handler for Reset button
	def reset(self):
	    # mark all letters unused
	    for l in string.uppercase:
		self.letters[l].config(state=ACTIVE)

	    # reset the lives, guesses and create a new target
	    self.lives=6
	    self.guesses = []
	    self.theTarget = self.getTarget()
    
	    # now reset the image and status
	    self.theImg.configure(file=self.firstImg)
	    txt = "Your target is:\n\t%s" % self.getResult()
	    self.status.configure(text=txt)

	# build the GUI here
	def displayStart(self):
		# create display frame with picture on left,
		# letters on right, picture goes inside a text widget
		d = Frame(self)
		
		# Text object will hold the image object.
		# Maybe this is not needed, recent documentation 
		# suggests Tk images can now hold gifs outside 
		# Text objects. 
		hm = Text(d, relief=SOLID, width=25, height=15)
		# now create an image object
		self.theImg = PhotoImage(file=self.firstImg) 
		# insert @ line 1, char 0
		hm.image_create('1.0', image=self.theImg) 
		hm.pack(side=LEFT, padx=20)

		# Create a Frame for the letter keys, each row 
		# of letters in its own nested Frame 
		ltr = Frame(d, border=1, relief=SUNKEN)
		for row in keys:
		    f = Frame(ltr)
		    for ch in row:
		        # create an event handler for this key
		    	action = lambda x=ch, s=self: s.display(x)
			self.letters[ch] = Button(f, text=ch, 
						width=2, 
						command=action)
			self.letters[ch].pack(side=LEFT)
		    f.pack(pady=1)
		ltr.pack(side=LEFT)
		d.pack()
		
		# Create control frame with status display left, 
		# Reset button middle and Quit button right
		c = Frame(self, border=1, relief=RAISED, background='blue')		
		txt = "Your target is:\n\t%s" % self.getResult()
		self.status = Label(c, anchor=W, 
				background='blue', foreground='yellow', 
				width=25, text=txt)
		self.status.pack(side=LEFT,  anchor=W)
		
		r = Button(c, text='Reset', padx=10, command=self.reset)
		r.pack(side=LEFT, padx=10, pady=5, anchor=W)
		
		q = Button(c, text='Quit', padx=10, command=self.quit)
		q.pack(side=RIGHT, padx=20, pady=5, anchor=W)

		c.pack()
		self.pack()

if __name__ == '__main__':
	hmGUI().play()
