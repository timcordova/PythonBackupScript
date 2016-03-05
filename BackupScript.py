#!/usr/bin/python
'''
SpyderOak, TrueCrypt, dis-mount, Backup Script 
@author: Tim C
'''
import os
import string
import datetime
import hashlib
FolderandFileLoc = "FolderandFileLoc"
SpiderOakPath = " " 
TrueCryptPath = " " 
LogFilepath = " " 
safefile = " "

def readconfigfile(SpiderOakPath,TrueCryptPath,LogFilepath,safefile, Setupfileopen):
    # This will read the configuration and assign path location
    now = datetime.datetime.now()
    holdstr = ""  
    for line in Setupfileopen:
        holdstr = str.split(line)
        if string.find(line,"SpiderOakPath") > -1: 
            SpiderOakPath = holdstr[1]
        elif string.find(line,"TrueCryptPath") > - 1:
            TrueCryptPath = holdstr[1]
        elif string.find(line, "LogFilepath") > -1:
            LogFilepath = holdstr[1]
        elif string.find(line,"safefile") > -1:
            safefile = holdstr[1]
            
    fo = open(LogFilepath,"a")  
    try:        
        fo = open(LogFilepath,"a") 
        fo.write (str(now) + "- Path Variable SpiderOakPath used -> " + SpiderOakPath + "\n")
        fo.write (str(now) + "- Path Variable TrueCryptPath used -> " + TrueCryptPath + "\n")
        fo.write (str(now) + "- Path Variable LogFilepath used -> " + LogFilepath + "\n")
        fo.write (str(now) + "- Path Variable hold used -> " + safefile + "\n")
    except: fo.error   
    shutdowntruecrypt(fo,now)
    copycontainer(fo,SpiderOakPath,TrueCryptPath,LogFilepath,safefile,now)
    fo.close    
    
    
def shutdowntruecrypt(fo,now):
    # Test to see if the truecypt is running 
    # If not then Shut it down
    foundstring = 0    
    try:
        f = os.popen( "ps ax" )
    except: os.error
    
    for line in f:
        if string.find(line, 'truecrypt') > -1:
            foundstring = 1
            break             
    
    if foundstring == 1:
        try:
            dismount = os.system("truecrypt -d")
            if dismount == 0:
                fo.write (str(now) + "- True Crypt0service found and the volume is dis-mounted \n"); 
            else:
                fo.write (str(now) + "- Failed to dismount service \n ");
        except: os.error 
    else:
        fo.write (str(now) + "- mount was not open \n "); 
     
def copycontainer(fo,SpiderOakPath,TrueCryptPath,LogFilepath,safefile,now):
    #Set Destination and Copy to new location
         
    Holddestfilesum = TrueCryptPath + safefile
    Holdorigfilesum = SpiderOakPath + "/" + safefile
    checksumdest = md5filecheck(Holddestfilesum)
    checksumorig = md5filecheck(Holdorigfilesum)
    
    
    runstring = "cp "  # This will only copy over updates to this file 
    runstring += TrueCryptPath 
    runstring += safefile       
    runstring += "  "
    runstring += SpiderOakPath  # This will only send over any updates to this file
    #if checksumdest <> checksumorig:
    testdiff = os.system("diff " + Holddestfilesum + " " + Holdorigfilesum)
 
    
    if testdiff !=0:
        try:
            os.system(runstring)
            testdiff = os.system("diff " + Holddestfilesum + " " + Holdorigfilesum)
            if testdiff != 0 :	    
                fo.write (str(now) + TrueCryptPath + safefile +  " File Copied to " + SpiderOakPath + "\n")
                fo.write(str(now) +  " ---- Processing Complete -------------------------------------------")
            else:
                fo.write(str(now) + TrueCryptPath + safefile + " File failed to copy " + SpiderOakPath + "\n")
        except: os.error
         
    else:
        fo.write (str(now) + " File has not been changed no copy was performed\n")
        
       
def md5filecheck(runstring):
    # This will get a md5 has of the file to determine if it changes - Truecypt is very good about time stamping its changes
        converted = hashlib.md5("").hexdigest()
        return(converted)
            
Setupfileopen = open(FolderandFileLoc,"r") 
readconfigfile(SpiderOakPath,TrueCryptPath,LogFilepath,safefile, Setupfileopen)
Setupfileopen.close() 

