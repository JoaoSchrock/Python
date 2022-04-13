#!/usr/bin/python
# I did this b'cos I had to transfer urls from the console (where I usally work)
# to X (to view the url in netscape)...and the gpm mouse copy/paste doesn't work
# between X and the console...read thru' the code and go figure !!
# sorry :o( !!!
# Usage: addurl <url>
# Needs a basic <HTML><BODY></BODY></HTML> html file existing at the path given
# by the variable 'file'

# If you check out a page in links (not a mis-spelling of lynx), but need to view it in 
# (for example) Netscape:
# a) Copy the url (using the mouse, ofcourse),
# b) Type 'addurl' at the prompt and paste the url as it's argument,
# c) addurl takes the argument, opens a html page (which I have prepared b'fore)
#    and adds the url as a link,
# d) Now I go into X and fire up netscape, which has been set to open up the html
# file with the links, and just click on the link...that's it.

file = raw_input("Digite o endereco do arquivo:\n>>> ")	# My file that has all the links, also the first
				# page Netscape opens, when I fire it up.
addr = raw_input("Endereco do link:\n>>> ")
view = raw_input("Palavra a ser mostrada:\n>>> ")
fl=open( file, 'r+' )
l=" ".join(fl.readlines()).split("</BODY>",1)[0]
escrito = l+"\t<a href="+addr+">\n\t"+view+"<br></a>\n </BODY>\n</HTML>\n"
fl.close()						
fl=open( file, 'w+')					
fl.write(escrito)
fl.close()
#
print "Adicionado o link para "+addr+" exibindo o texto "+view+" no arquivo, "+file+"."
exiting = raw_input("Programa encerrado. Pressione ENTER para sair.")
							#
# <HTML>	<---------------------------------------# File sample
# <HEAD><TITLE>File's called urls.html</TITLE></HEAD>
#  <BODY>
# 	<a href=http://www.cs.cf.ac.uk/Dave/C/>
#	http://www.cs.cf.ac.uk/Dave/C/<br></a>
# 	<a href=http://www.itknowledge.com/reference/archive/1571690638/>
# 	http://www.itknowledge.com/reference/archive/1571690638/<br></a>
# 	<a href=http://utopia.knoware.nl/users/damon/download.htm>
# 	http://utopia.knoware.nl/users/damon/download.htm<br></a>
# 	<a href=ftp://ftp.gams.at/pub/linux/isp/>
#	ftp://ftp.gams.at/pub/linux/isp/<br></a>
# 	<a href=http://www.cs.bgu.ac.il/~omri/Humor/evolution.html>
# 	http://www.cs.bgu.ac.il/~omri/Humor/evolution.html<br></a>
# 	<a href=http://www.crosswinds.net/~agauld/tutor.zip>
# 	http://www.crosswinds.net/~agauld/tutor.zip<br></a>
# 	<a href=http://acm.uva.es/problemset>
#	http://acm.uva.es/problemset<br></a>
# 	<a href=http://w1.132.telia.com/~u13208596/index.htm>
# 	http://w1.132.telia.com/~u13208596/index.htm<br></a>
# 	<a href=http://216.239.37.100>
#	google.com<br></a>
# 	<a href=http://py-howto.sourceforge.net/regex/>
# 	http://py-howto.sourceforge.net/regex/<br></a>
# 	<a href=http://w1.132.telia.com/~u13208596/index.htm>
# 	http://w1.132.telia.com/~u13208596/index.htm <br></a>
# 	<a href=http://www.faqts.com/>
#	http://www.faqts.com/<br></a>
# 	<a href=http://www-gnats.gnu.org:8080/doc/info2www/>
# 	http://www-gnats.gnu.org:8080/doc/info2www/<br></a>
# </BODY>
# </HTML>
#
#
#Modicicacoes para facilitar o uso feitas por Bruno Moreira Guedes
#
