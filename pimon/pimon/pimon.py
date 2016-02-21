###############################################################################
# pimon is used as the main process by which a raspberry pi is put into       #
# combination monitor/sftp uploading mode. Two wireless cards are required.   #
# pimon is not smart enough to distinguish special adapter names.             #
# All it knows are wlan0 and wlan1. pimon is lazy and makes extenisve         #
# use of the subprocess call.                                                 #
# Plans for pimon                                                             #
# 1 - Smartly determine systemd service controllers                           #
# 2 - Smartly determine wireless cards with grep then python libs.            #
# 3 - Dyanmically create certificates, .conf files for stunnel and ovpn       #
#         by asking the server nicely.                                        #
# 4 - Integrate pysftp instead of subprocess.                                 #
# 5 - Replace most or all subprocess calls with actual, *for real*, libs.     #
###############################################################################

import os
import subprocess
import time



def pingTest(attempts, address):
	
    #Did the attempt string pass?
	print("Ping attempts set to: %s" % attempts)
	
    #Did the address string pass?
	print("IP Address set to: %s" % address)
	
    #Long command to run a ping
	pingTest = subprocess.Popen('ping -c %s %s' % (attempts, 
	address), shell=True)

    #Wait until pings
	time.sleep(5)
	
    #This will set pingTest as a boolean int (0 or 1)
    #I will now procede to clobber my variable
	pingTest = pingTest.wait()
	
    #This returns 1 or 0 to the main program.
	return pingTest

def startEscape(ssid):
    #If all you have is a hammer...
    print("ssid set to: %s" % ssid)

    #bring up interface
    wlanUp = subprocess.Popen('netctl start %s' % (ssid),
    shell=True)

    time.sleep(20)

    wlanUp = wlanUp.wait()

    #Start stunnel
    stunnel = subprocess.Popen('systemctl start stunnel', 
    shell=True)
    
    time.sleep(5)

    stunnel = stunnel.wait()

    #Start openvpn client configuration
    openvpn = subprocess.Popen('systemctl start openvpn@client', 
    shell=True)
    
    time.sleep(5)
    
    openvpn = openvpn.wait()
    
    #Returns tuple of values)
    
    return (wlanUp, stunnel, openvpn)

def stopEscape(ssid):
    #This is just start escape in reverse order
    #Stop openvpn
    openvpn = subprocess.Popen('systemctl stop openvpn@client', 
    shell=True)
    
    time.sleep(5)
    
    openvpn = openvpn.wait()
    
    #Stop Stunnel
    stunnel = subprocess.Popen('systemctl stop stunnel', 
    shell=True)
    
    time.sleep(5)

    stunnel = stunnel.wait()

    #Bring down interface   
    wlanUp = subprocess.Popen('netctl stop %s' % (ssid),
    shell=True)

    time.sleep(20)

    wlanUp = wlanUp.wait()
    
    #return tuple of values
    return (wlanUp, stunnel, openvpn)

def monitorMode(state, interface):
    #State is start or stop
    #interface is wlanX

    #Begin monitor mode for specified interface
    monitorMode = subprocess.Popen('airmon-ng %s %s' % (state, 
    interface), shell=True)
    
    #clobber
    monitorMode = monitorMode.wait()
    
    #return
    return monitorMode


def gatherData():
    
    prompt = '> '
    
    print("Please input the desired values for tcpdump")
    print("What is the name of the process screen?")
    screenName = input(prompt)
    
    print("How long in seconds will tcpdump capture?")
    capTime = input(prompt)
    
    print("Which interface will tcpdump use? Hint: wlan1mon")
    interface = input(prompt)
    
    print("How many pcap files will tcpdump make?")
    print("Note that file number*capturetime is total time.")
    fileQuanitity = input(prompt)
    
    print("What will the pcap sequence be named?")
    fileName = input(prompt)
    
    print("Beginning capture...")

    gatherData = subprocess.Popen('screen -S %s tcpdump -G %s -s 0 -i %s -W %s -w %s.pcap' 
    % (screenName, capTime, interface, fileQuanity, fileName), shell=True)

    gatherData = gatherData.wait()

    return gatherData