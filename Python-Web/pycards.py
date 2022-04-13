#######################################################################################
####### Giombetti.com takes to garantie for the correct working of this script. #######
################## If you have questions mail to joseluis@vexa.net ####################
#######################################################################################
#######################################################################################
########################### Made by Jose Luis Garduno #################################
################### Thanks to Marc Giombetti for making Phpcards ######################
#######################################################################################
#######################################################################################
##########################  Function to upload files   ################################
#######################################################################################

def subir_archivos():
	import ftplib
	print "Wait while the files are uploaded..."
	ftp = ftplib.FTP(sitioftp)
	ftp.login(user=usuario,passwd=password,acct=cuenta)
	ftp.cwd(directoriotxts)
	if directorio + ".txt" not in ftp.nlst():
		archivodonde = open(donde2,'r')
		ftp.storlines('STOR ' + directorio + ".txt",archivodonde)
		print "Configuration File uploaded..."
		continuar = "s"
	else:
		continuar = raw_input("Configuration file already exists,do you want to continue and upload the pictures?(y/n): ")
	if continuar <> "n":
		ftp.cwd(directoriofotos)
		if directorio not in ftp.nlst():
			ftp.mkd(directorio)
			ftp.cwd(directorio)
			for x in arr:
				archiviyo = open(donde + x,"rb") 
				ftp.storbinary('STOR ' + x,archiviyo)
				archiviyo.close()
				print   x + " was uploaded "
		else:
			"directory already exists"
	ftp.close()

#######################################################################################
##########################      Programa Principal   ##################################
#######################################################################################

sitioweb = 'www.yourserverhere.com'
sitioftp = 'ftp.yourserverhere.com'
usuario = 'ftpuser'
password = 'ftppass'
cuenta = usuario
directoriotxts = '/htdocs/www/pictures/txt/'
directoriofotos = '/htdocs/www/pictures/'
webfotos = 'http://www.yourserverhere.com/fotos/'

import os
print "pccfmpu - php cards configuration file maker and picture uploader"
print "This is happyware, you have to smile while using this program"
print "\n \n"
evento = raw_input("Title: (example. Party at Joes) \n")
directorio = raw_input("In which directory are the pictures located? (example. joesparty)\n")
print
donde = os.getcwd() + "\\" + directorio + "\\"
arr = os.listdir(donde)
popo = []
popo.append("{" + evento + '};' + webfotos + directorio + '/; \n')
for x in arr:
	if x <> "Thumbs.db":
		popo.append(x + ";\n")
for x in popo:
    print x
donde2 = donde + directorio + ".txt"
archivo = open(donde2,'w') 
archivo.writelines(popo)
archivo.close()

subir = raw_input("Do you wish to upload the whole thing to the internet: (s/n)")
if subir <> "n":
	subir_archivos()
	
else:
	print "You choose not to upload the files, do it manually"
	
salida = raw_input("\n \n Press ENTER to quit")


