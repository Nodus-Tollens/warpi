import glob
import os
import random
import time
import shutil
import threading
from threading import Thread as process
from subprocess import check_output
import Tkinter as tk 

def get_pid():
	frame.config(bg='#C5C7D4')
	dapid = check_output(["pidof","kismet_server"])
	up("KISMET OFFLINE")
	killcmd = "kill -9 " + dapid
	os.system (killcmd )
	time.sleep (3)
	copynetxml()

def setmon():
	up ("ACTIVATE MONITOR MODE ")
	setmoncmd="sudo airmon-ng start wlan1"
	os.system (setmoncmd)
	time.sleep(1)

def setgps():
	up ("GPS ONLINE ")
	setgpscmd="gpsd /dev/ttyUSB0"
	os.system (setgpscmd)
	time.sleep(1)

def startkis():
	frame.config(bg="Green")
	up ("KISMET ONLINE")
	#startkiscmd = "kismet -c wlan1mon"
	startkiscmd = "kismet_server -c wlan1mon --use-gpsd-gps"
	os.system (startkiscmd)
	

def up(txt):
	#lab=dtxt.get()
	#lab += txt + "\r"
	dtxt.set(txt)

def kischk():
	try:
		dapid = check_output(["pidof","kismet_server"])
		kis_stat ="Kismet Server running on pid:" + dapid
		return True
	except:
	  	kis_stat = "No instance Kismet Server found"
		return False

def kis_Switch():
	if(kischk() == True):
		#print("Kismet is running -->  Turn it off.")
		get_pid()
	else:
		#print("Kismet is NOT running  --> Turn it on")
		startkis()
	
def copout():
	copoutcmd = "rclone copy " + outf + " remote:KML"
	print copoutcmd
	os.system (copoutcmd)

def Initialize():
	frame.config(bg="Yellow")
	up ("INITIALIZE")
	setgps()
	setmon()
	frame.config(bg='#C5C7D4')
	up("WAR DRIVE READY")



def copynetxml():
	files = glob.iglob(os.path.join("/home/pi/PY", "*.netxml"))
	for file in files:
    		if os.path.isfile(file):
        		shutil.copy2(file, './NETXML')


def uptodrive():
	frame.config(bg="Blue")
	up("UPLOADING NETXML")
	copoutcmd = "rclone copy './NETXML' remote:NETXML"
	print copoutcmd
	os.system (copoutcmd)
	frame.config(bg='#C5C7D4')
	up("UPLOAD COMPLETE")




def backitup():
	exts="*.alert", "*.gpsxml", "*.nettxt", "*.netxml", "*.pcapdump"
	for ext in exts:
		dirpath = os.getcwd()
		print (dirpath)
		files = glob.iglob(os.path.join(dirpath, ext))
		for file in files:
			print file[9:]
			dest = "./BKUP/" + file[12:]
			trimdest = dest.replace("-","") 
			print (trimdest) 
    			if os.path.isfile(file):
        			shutil.copyfile(file, trimdest )


def cleanitup():

	frame.config(bg="Red")
	up(" ")
	backitup()
	exts="*.alert", "*.gpsxml", "*.nettxt", "*.netxml", "*pcapdump"
	dirpath = os.getcwd()	
	for ext in exts:
		files = [file for file in glob.glob(dirpath +"/"+ ext)]
		for file in files:
    			print "deleting " + file
			os.remove(file)
	frame.config(bg='#C5C7D4')
	up("SYSTEM PURGED")





root = tk.Tk()
root.geometry('1024x600')

photo1 = tk.PhotoImage(file = "minihack.png") 
photo2 = tk.PhotoImage(file = "diff.png") 
photo3 = tk.PhotoImage(file = "cloud.png") 
photo4 = tk.PhotoImage(file = "clean.png") 


b0=tk.Button(root,text="  INITIALIZE", command=lambda: process (target = Initialize).start (), image = photo1, compound='left', font =( 'Segoe UI', 15))
b0.place(relheight=0.25, relwidth=.5)

b1=tk.Button(root,text="  WAR DRIVE", command=lambda: process (target = kis_Switch).start (), image = photo2, compound='left', font =( 'Segoe UI', 15))
b1.place(relx=0.5, relheight=0.25, relwidth=.5, )

b2=tk.Button(root,text="  UPLOAD DATA", image = photo3,command=lambda: process (target = uptodrive).start (), compound='left', font =( 'Segoe UI', 15))
b2.place(rely=0.25, relheight=0.25, relwidth=.5)

b3=tk.Button(root,text="  CLEAN UP", command=lambda: process (target = cleanitup).start (), image = photo4, compound='left', font =( 'Segoe UI', 15))
b3.place(relx=0.5,rely=0.25, relheight=0.25, relwidth=.5)

frame= tk.Frame(root, bg='#C5C7D4', bd=10)
frame.place(rely=0.50, relx=0, relheight=0.50, relwidth=1)

dtxt = tk.StringVar()
label = tk.Label(frame, fg='#04e043',bg='#242322',font =( 'Segoe UI', 24), anchor='c', bd=10, textvariable = dtxt)
label.place(relheight=1, relwidth=1)




root.mainloop() 

