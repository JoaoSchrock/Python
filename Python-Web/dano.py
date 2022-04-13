#!../CGIpython/cgipython

########################################################################
# Logger script based on Matt's Perl "Book 'Em Dano" script
# Original perl script available from http://worldwidemart.com/scripts
#
# This variant by L.Pritchard 2001: For free distribution and use
# This script is intended to be run as a server side include using 
# <!--#include virtual="/pathto/dano.py"--> or
# <!--#exec cgi="/pathto/dano.py"-->
# I find best use by linking to the script as an image of size 0, which 
# gets around problems with the server being noEXEC, and the cgi-bin 
# directory not being reachable other than by URL, as follows:
# <IMG SRC="http://pathto/dano.py?referringpage" BORDER=0 WIDTH=0 ALT="">
#
# The script can be called with any number of arguments - they are just 
# appended to the log file so you can index the page the call came from 
# and track people's movements around your site
#
# The script logs as follows
# argument : time
# remote address : browser : referring page
# 
# You can exclude your own site (and others) from consideration by adding 
# the IP number to the exc_list list
#########################################################################

import os, sys, string

logfilename = "/absolute/path/to/log/file/directory/"
# change the directory path

exc_list = ["xxx.xxx.xxx.xxx", "xxx.xxx.xxx.xxx"]
#exc_list = []
# the list of machines to exclude from logging

######### And now the tricky bit #############

# Get input
infolist = sys.argv[1:] + [ os.popen('date').read(),
                         os.environ.get("REMOTE_ADDR", "--noaddr--"),
                         os.environ.get("HTTP_USER_AGENT", "--noagent--"),
                         os.environ.get("HTTP_REFERER", "--noreferer--"),
                         '\n']

# print infolist
out = string.join(infolist, ' : ')

address = os.environ.get("REMOTE_ADDR", "noaddr")

logfilename += (address + ".dat")

if address not in exc_list:
    open(logfilename,'a').write(out)

print "Content-type: text/html\n\n"   

