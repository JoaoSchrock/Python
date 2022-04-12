
#
# Python Hyperschema is placed in the public domain by Randy Phillips
# (hyperschema@rebeccaphillips.com) because you will need to edit this
# code to suit your own tastes on the HTML output.  If I release it 
# under the GPL that would be a real pain in the neck, as the GPL 
# requires that you giving me every single one of your code changes.
#
# This program was originally written in C.  The Python version
# is much smaller, certainly I enjoyed the translation from C
# to Python!  Future improvements I'd like to see are direct data
# dictionary reads and a GUI front end.  I'll be working on it.
#
# If you find a bug or would like to make a contribution to the code,
# please let me know.  Bug fixes and enhancements are most welcome!
# I would like to put on the hyperschema web site a list of users
# and developemnt contributors, please let me know if you use this
# public domain source code.
#
# Email me with any questions or comments, and enjoy!
#

import sys, string




version = "3.0"
copyright_string = "Your copyright statement, if any, goes here."




#
# initialize empty data structures to make sure they start empty
#
table_list = [] # list of all tables in the input file
table  = {} # dictionary holding data for one table in the schema
column = {} # dictionary holding data for one column in a table
column_start_positions = [] # positions of column data in input file
column_end_positions   = [] # positions of column data in input file




#
# Simple introduction
#
print
print "Python Hyperschema " + version + " - the open source"
print "relational database schema hypermapper"
print




#
# open the named file for input
#
if len(sys.argv) > 1:
    filename = sys.argv[1] # for command line input
else:
    print "Enter the name of a data file"
    filename = string.rstrip(sys.stdin.readline()) # for development (rstrip for !#&%!! Windoze)
    print
f = open(filename, 'r')

print "Opened " + filename + " for input"




#
# iterate through all lines in the input file containing data
# to find the spool file's dashed line - denotes column width and position information
#
temp_line = f.readline()
while temp_line:
    if temp_line[0] == "-":
	break
    temp_line = f.readline()

print "Found dashed line in input file"

	
	
	
#
# analyze the dashed line, storing the column start and end positions
#
column_start_positions.append(0)
for i in range(len(temp_line)-1):
    if i == 0:
    	continue
    if ((temp_line[i] == ' ') or (temp_line[i+1] == '\n') or (temp_line[i+1] == '\r')) and (temp_line[i-1] == '-'):
    	column_end_positions.append(i)
    	if (temp_line[i+1] != '\n') and (temp_line[i+1] != '\r'):
    	    column_start_positions.append(i+1)

print "Determined column positions from dashed line"




#
# read input file data
#
temp_line = f.readline()
table['name'] = string.lstrip(string.rstrip(temp_line[column_start_positions[0]:column_end_positions[0]]))
templist = []
while temp_line:
    if len(temp_line) < 3: # after this there is no more data, takes care of all operating system end-of-lines
    	break
    	
    # if this is a new table, save the old one to the table list and update - does NOT work for last table!
    if table['name'] != string.lstrip(string.rstrip(temp_line[column_start_positions[0]:column_end_positions[0]])):
        table['columns'] = templist
    	table_list.append(table)
    	templist = [] # empty the templist
    	table = {} # empty the table
    	table['name'] = string.lstrip(string.rstrip(temp_line[column_start_positions[0]:column_end_positions[0]]))
    	
    # read all data into the table list
    column['name']             = string.lstrip(string.rstrip(temp_line[column_start_positions[1]:column_end_positions[1]]))
    column['data_type']        = string.lstrip(string.rstrip(temp_line[column_start_positions[2]:column_end_positions[2]]))
    column['data_length']      = string.lstrip(string.rstrip(temp_line[column_start_positions[3]:column_end_positions[3]]))
    column['data_precision']   = string.lstrip(string.rstrip(temp_line[column_start_positions[4]:column_end_positions[4]]))
    column['data_scale']       = string.lstrip(string.rstrip(temp_line[column_start_positions[5]:column_end_positions[5]]))
    column['default_length']   = string.lstrip(string.rstrip(temp_line[column_start_positions[6]:column_end_positions[6]]))
    column['nullable']         = string.lstrip(string.rstrip(temp_line[column_start_positions[7]:column_end_positions[7]]))
    column['key_type']         = string.lstrip(string.rstrip(temp_line[column_start_positions[10]:column_end_positions[10]]))
    column['fkey_table_name']  = string.lstrip(string.rstrip(temp_line[column_start_positions[12]:column_end_positions[12]]))
    column['fkey_column_name'] = string.lstrip(string.rstrip(temp_line[column_start_positions[13]:column_end_positions[13]]))
    templist.append(column)
    column = {} # empty the column
    temp_line = f.readline()
    
# finish up the last table
table['columns'] = templist
table_list.append(table)

print "Read in all data from input file"




#
# It is possible for a primary key to also be a foreign key.  In the data file we read,
# this results in two rows with the same name - one a primary key, and one a foreign key.
# Here we find these and flag them for special processing later.
#
for table_iter in table_list:
    for column_iter1 in table_iter['columns']:
    	for column_iter2 in table_iter['columns']:
    	    if (column_iter1 != column_iter2) and (column_iter1['name'] == column_iter2['name']):
    	        if column_iter1['key_type'] == "P":
    	            column_iter1['key_type'] = "I" # ignore this entry, use "B" immediately below
    	            column_iter2['key_type'] = "B" # "B" for both primary key and foreign key

print "Checked all tables for primary keys that are also foreign keys"




#
# For each table, populate the list of foreign keys pointing to this table
#
for table_iter1 in table_list:
    table_iter1['fkeys'] = {}
    templist = [] # empty the templist
    for table_iter2 in table_list:
        for row_iter in table_iter2['columns']:
            if row_iter['fkey_table_name'] == table_iter1['name']:
                temp_fkey = {}
		temp_fkey['table_name']     = table_iter2['name'] # table name
		temp_fkey['column_name']    = row_iter['name'] # column name
		templist.append(temp_fkey)
    table_iter1['fkeys'] = templist

print "Created lists of foreign keys for all tables"		




#
# make the index HTML page
#
f = open("index.html", "w")

f.write("<HTML><head><title>Hyperschema - Master Index</title></head>\n")
f.write("<BODY bgcolor=\"#ffffff\" text=\"#000000\" link=\"#0000a0\" vlink=\"#800080\" alink=\"#ff0000\">\n")
	
# header
f.write("<A NAME=\"Top\">\n")
f.write("<CENTER><B>- <A HREF='http://hyperschema.sourceforge.net'>Python Hyperschema</A> ")
f.write(version + " -<BR><BR><FONT SIZE=+1>Master Index of Tables</FONT></B></CENTER><BR>\n")
	
# Make alphabetical quick-pick headings
f.write("<CENTER>")
f.write("<A HREF=\"#quick_" + table_list[0]['name'][0] +"\">" + table_list[0]['name'][0] + "</A>")
for i in range(len(table_list)-1):
    if table_list[i+1]['name'][0] != table_list[i]['name'][0]:
	f.write(" &nbsp;&nbsp;&nbsp;<A HREF=\"#quick_" + table_list[i+1]['name'][0] +"\">" + table_list[i+1]['name'][0] + "</A>")
f.write("</CENTER><BR>\n")
	
# populate index, adding internal bookmarks for quick_picks at top of list
f.write("<TABLE ALIGN=\"CENTER\" cellpadding=\"3\">\n")
f.write("<TR><TD><BR><BR><CENTER>")
f.write("<A NAME=\"quick_" + table_list[0]['name'][0] + "\"><A HREF=\"#Top\">Back to Top</A></CENTER>")
f.write("<BR><BR><A HREF=\"" + table_list[0]['name'] + ".html\">" + table_list[0]['name']  + "</A></TD></TR>\n")
for i in range(len(table_list)-1):
    if table_list[i+1]['name'][0] != table_list[i]['name'][0]: # new quick-pick found, add bookmark
	f.write("<TR><TD><BR><BR><CENTER>")
	f.write("<A NAME=\"quick_" + table_list[i+1]['name'][0] + "\"><A HREF=\"#Top\">Back to Top</A></CENTER>")
	f.write("<BR><BR><A HREF=\"" + table_list[i+1]['name'] + ".html\">" + table_list[i+1]['name']  + "</A></TD></TR>\n")
    else:
	f.write("<TR><TD><A HREF=\"" + table_list[i+1]['name'] + ".html\">" + table_list[i+1]['name'] + "</A></TD></TR>\n")
f.write("</TABLE><BR>")
	
# footer
f.write("<BR><BR><CENTER><FONT SIZE=-1>\n")
f.write("<A HREF='http://hyperschema.sourceforge.net'>Python Hyperschema</A> ")
f.write(version + " is brought to you by <A HREF='http://www.epenergy.com'>El Paso Energy</A>'s<BR>\n")
f.write("<IMG SRC=\"prodsup.gif\"><BR><BR>\n")
f.write(copyright_string + "\n")
f.write("</FONT></CENTER>\n")

# padding the bottom of the pages with returns helps the bottom tables look nice
for i in range(35):
    f.write("<BR>\n")
	
f.write("</BODY></HTML>\n")
f.close()

print "Completed master index page"
	



#
# make individual HTML pages, one per schema table	
#
print "Creating individual HTML pages"
for table_iter in table_list:
    filename = table_iter['name'] + ".html"
    print "     Creating " + filename
    f = open(filename, "w")
    
    f.write("<HTML><head><title>Python Hyperschema " + version + " - " + table_iter['name'] + "</title></head>\n")
    f.write("<BODY bgcolor=\"#ffffff\" text=\"#000000\" link=\"#0000a0\" vlink=\"#800080\" alink=\"#ff0000\">\n")
    f.write("<div id=\"overDiv\" style=\"position:absolute; visibility:hide;z-index:1;\"></div>\n")
    f.write("<SCRIPT LANGUAGE=\"JavaScript\" SRC=\"overlib.js\"></SCRIPT>\n")
    
    # header
    f.write("<A NAME=\"Top\">\n")
    f.write("<A HREF=\"index.html\">Master Index</A>\n")  # top left corner
    f.write("<CENTER><B><FONT SIZE=+2>" + table_iter['name'] + "</FONT></B></CENTER><BR>\n")
    
    if len(table_iter['fkeys']) == 0:
	f.write("<CENTER>No foreign keys point to this table.</CENTER><BR>\n")
    else:
    	f.write("<CENTER><A HREF=\"#fkeys\">Foreign keys pointing to this table:</A></CENTER><BR>\n")
    	
    f.write("<TABLE ALIGN=\"CENTER\" BORDER=\"1\" cellpadding=\"3\">\n")
    f.write("<TR BGCOLOR=\"#D0D0D0\"><TH>Column Name</TH><TH>Data Type</TH><TH>Nullable</TH></TR>\n")

    for column_iter in table_iter['columns']:
	if column_iter['key_type'] != "I": # if column is not ignored above
	    f.write("<TR><TD>")

	    if column_iter['key_type'] == 'P': # primary key, font size +1 and bold
		f.write("<FONT SIZE=+1><B>" + column_iter['name'] + " </B></FONT><FONT SIZE=-1>(primary key)</FONT>\n")
		
	    elif column_iter['key_type'] == 'R': # foreign key, make javascript output for mouseover
		f.write("<A HREF=\"" + column_iter['fkey_table_name'] + ".html\" ")
		f.write("onMouseOver=\"overlib('This foreign key is <B>")
		f.write(column_iter['fkey_table_name'] + "." + column_iter['fkey_column_name'])
		f.write("</B>')\" onMouseOut=\"nd()\">" + column_iter['name'] + "</A>\n")

	    elif column_iter['key_type'] == 'B': # both primary key and foreign key, make javascript output for mouseover
		f.write("<A HREF=\"" + column_iter['fkey_table_name'] + ".html\" ")
		f.write("onMouseOver=\"overlib('This primary key is <B>")
		f.write(column_iter['fkey_table_name'] + "." + column_iter['fkey_column_name'])
		f.write("</B>')\" onMouseOut=\"nd()\">" + column_iter['name'] + "</A>\n")
		
	    else:
		f.write(column_iter['name'] + "\n")
		    
	    # data type
	    f.write("</TD><TD>" + column_iter['data_type'])
	    if column_iter['data_type'] == "NUMBER":
		if len(column_iter['data_precision']) > 0: # not all numbers have precision specifications
		    f.write("&nbsp;&nbsp;(" + column_iter['data_precision'] + "," + column_iter['data_scale'] + ")")
	    if column_iter['data_type'] == "VARCHAR2":
		f.write("&nbsp;&nbsp;[" + column_iter['data_length'] + "]")
	    f.write("\n");
		    
	    if column_iter['nullable'] == "N":
		f.write("</TD><TD><CENTER>No</CENTER></TD></TR>\n")
	    else:
		f.write("</TD><TD><CENTER>Yes</CENTER></TD></TR>\n")


    f.write("</TABLE><BR>\n");
    f.write("<BR><BR>\n");

    if len(table_iter['fkeys']) > 0:
	f.write("<A NAME=\"fkeys\"></A><A HREF=\"#Top\">Back to top</A><CENTER>Foreign keys pointing to ")
	f.write ("<B>" + table_iter['name'] + "</B>:</CENTER><BR>\n")
	
	f.write("<TABLE ALIGN=\"CENTER\" BORDER=\"1\" cellpadding=\"3\">\n")
	f.write("<TR BGCOLOR=\"#D0D0D0\"><TH>Table Name</TH><TH>Column Name</TH></TR>\n")

	for fkey_iter in table_iter['fkeys']:
	    f.write("<TR><TD><A HREF=\"" + fkey_iter['table_name'] + ".html\">")
	    f.write(fkey_iter['table_name'] + "</A></TD><TD>" + fkey_iter['column_name'] + "</TD></TR>")

	f.write("</TABLE><BR>\n");
		
    # footer
    f.write("<BR><BR><CENTER><FONT SIZE=-1>\n")
    f.write("<A HREF='http://hyperschema.sourceforge.net'>Python Hyperschema</A> ")
    f.write(version + " is brought to you by <A HREF='http://www.epenergy.com'>El Paso Energy</A>'s<BR>\n")
    f.write("<IMG SRC=\"prodsup.gif\"><BR><BR>\n")
    f.write(copyright_string + "\n")
    f.write("</FONT></CENTER>\n")

    # padding the bottom of the pages with returns helps the bottom tables look nice
    for i in range(35):
        f.write("<BR>\n")

    f.write("</BODY></HTML>")
    f.close()




print "Done!"












