import socket
from subprocess import check_output
from scenarioHandler import *


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def setupServer():
    print ("Socket created")
    
    host= check_output(['hostname','-I'])
    port=5560
	
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    return s

def setupConnection():
    s.listen(1) # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

def receiveMessageAndParse(conn):
    while True:
            try:
                data = conn.recv(1024)
                data = data.encode("utf-8")
		print("Received data=",data)
            except:
                # happens when connection is reset from the peer
                print("Connection reset")
		break
            
            if data == "quit":
                #quit command to regulary disconnect
		print("Quit current connection")
                break
            
            parseMessage(data)

def sendFile(filePath):
    file = open(filePath, 'r')
    data=file.read(1024)
    
    while(data):
        s.send(data)
        data=file.read(1024)
        
def sendStatusFiles():
    sendFile('output.log')
    sendFile('error.log')

def getWifiIPAddress():    
     wifi_ip = check_output(['ifconfig', '$wlan | grep -q "inet addr:"'])
     return wifi_ip
