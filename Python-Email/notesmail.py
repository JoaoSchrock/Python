## A simple hack to send Lotus Notes email from Python
## Tested using Python 2.1 on Windows 2000 with Notes 4.66c 
## by Brian Dorsey (updated 8/8/2001)
## brian@dorseys.org
##
## This is a barebones, simple way to send email with an arbitrary number of attachments.
## I experimented until it worked and then stopped. This is probably not the most 
## efficient way to do this (and I'm a newbie to Python as well!). If you have 
## any ideas, please send them my way!
##
## I'm not sure how well this may or may not work for anyone else, but it's 
## been working for me for a few months.
##
## This will send email from the currently active Notes account, and ask you for a 
## password if you're not logged in - so, it would probably need some kind of 
## modification to be used unattended on a server somewhere... 
##
## If you want to extend this, you can find more documentation on the Notes COM API
## at http://www.lotus.com/developers/devbase.nsf/homedata/homecom 
## a windows help version can be had by following the "Download Now" link on that 
## page and scrolling to the bottom of the page.
## (There may be better stuff out there, this is just the first thing I found. ;)
##
##
## Sample interactive test session: 
## Python 2.1 (#15, Apr 16 2001, 18:25:49) [MSC 32 bit (Intel)] on win32
## Type "copyright", "credits" or "license" for more information.
## >>> import notesmail
## >>> notesmail.sendEmail(subject='Hello from Python!', body='Test message')
## >>> #Check your email, you should have a new message!
## ...
## >>> notesmail.sendEmail(subject='Hello from Python!', body='Test message', attac
## hments=['c:/Python21/README.txt']) #choose a file which exists on your system...:)
## >>> #Check it again, you should have a new email with the file attached!
## 

def sendEmail(recipients=[], subject='', body='', attachments=[]):
	"""Use Notes to send an email from the current user
	
	recipients -- a list of email addresses to send to 
		(or full names from the notes address book)
	subject -- a string containing the subject of the email
	body -- a string containing the body text of the email 
		(empty lines didn't seem to come through properly for me, I had to 
		include at least a space on each line to keep them from disappearing.)
	attachments -- a list of full path and filenames to attach to the email"""
	
	import win32com.client
	sess=win32com.client.Dispatch("Notes.NotesSession")
	db = sess.getdatabase('','')
	db.openmail
	doc=db.createdocument
	
	#Set the recipient to the current user as a default
	if not recipients:
		recipients = sess.UserName  
		
	doc.SendTo = recipients
	doc.Subject = subject
	doc.Body = body
	
	#Notes attachments get made in RichText items...
	if attachments:
		rt = doc.createrichtextitem('Attachment')
		for file in attachments:
			rt.embedobject(1454,'',file)
	doc.Send(0)
	
	
if __name__ == '__main__':
	#Send a simple test email to the current Notes user
	#sendEmail()
	sendEmail(subject='Test email from Python!', body='This has been a test, and only a test.')		
	