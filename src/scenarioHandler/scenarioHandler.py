from valueHolder import *
from messageHandler import *
from displayHandler import *
from messageReceiver import *
import atexit
import time

from subprocess import check_output


spi= None
            
display=displayHandler(30)

addSubValue=0

def main():
    #time.sleep(10)
    
    init_spi()
    
    while getWifiIPAddress() is None:
        print("Wifi not connected")
	showWifiConnectionError()
	time.sleep(60)
            
    
    #start timer thread, which periodically updates MovingBar
    display.displayData()
    
    #bind tcp socket
    #host_ip = getWifiIPAddress()
   # port = 5560
	
    setupServer()
    atexit.register(exitHandlerFunction)
 
    while True:
        setupConnection()
        receiveMessageAndParse()
    
     
    
def getWifiAddress2():
    wifi_ip = check_output(['ifconfig','$wlan0 |grep "inet addr"'])
    print("length=",len(wifi_ip))
    if wifi_ip.isspace() or not wifi_ip:
        return None
    else:
        print("wifi address found:",wifi_ip)
	return wifi_ip
	
def getWifiIPAddress():    
    host_ip= check_output(['hostname','-I'])
    if host_ip.isspace() or not host_ip:
        print("no host ip found")
        return None
    else:
	return host_ip
	
        
def showWifiConnectionError():
    setSingleAnimation("PULSESLOW", "A", NUMBER_LEDS, 10000, colors['red'])  #show warning, if url unreachable
    setSingleAnimation("PULSESLOW", "B", NUMBER_LEDS, 10000, colors['red'])
    setSingleAnimation("PULSESLOW", "C", NUMBER_LEDS, 10000, colors['red'])
    setSingleAnimation("PULSESLOW", "D", NUMBER_LEDS, 10000, colors['red'])
	      

#DISPLAY:SIDE//DIPLAYCOLOR//REFCOLOR//REFERENCEVALUE//STEPSIZE//MODE//BRIGHTNESS//URL//PATHXML//PATHJSON    #TODO: RANGEMAPPING
#SET:SAMPLETIMEDELAY//BRIGHTNESS


def parseMessage(message):
    print("Parsing message:" , message)  #log file
    messageLength= len(message)
    seperatorIndex=message.index(':')
    
    mode= message[0:seperatorIndex]
    values= message[seperatorIndex+1:messageLength]
    values = values.split("//")
    print(values)
    
    if mode == "DISPLAY":
        side=values[0]
        displayColor=values[1]
        referenceColor=values[2]
        referenceValue=float(values[3])
        stepSize=float(values[4])
        mode=values[5]
        
        requestURL=values[6]
    
        
        pathXML=None
        pathJson=None
        
        if(values[7] is not "null"):
            pathXML=values[7].split(",")
            print "pathXML=",pathXML
        if(values[8] is not "null"):
            pathJson=values[8].split(",")
            print "pathJSON", pathJson  
        
        if(pathJson is not None):
            addNewValueObject(side,displayColor,referenceColor,referenceValue,stepSize,mode,requestURL,pathXML,None)
        elif(pathXML is not None):
            addNewValueObject(side,displayColor,referenceColor,referenceValue,stepSize,mode,requestURL,None,pathJson)
        else:
            printError("No path to value in either xml or json.") #error log
    
    if mode=="SET":
        delay= int(values[0])
        brightness=int(values[1])
        
        if delay is not "null":
            display.delay=delay
        if brightness is not "null":
            setBrightness(brightness)
                  


def scaleValue(value): #TODO: scale value, e.g. distribution,intervalls
    
    return value
    

def scaleFunctionRain(millimeterPerHour):
    if(millimeterPerHour<2.5):
        return 1
    elif(millimeterPerHour<7.6):
        return 2
    elif(millimeterPerHour<30):
        return 3
    else:
        return 4

#DISPLAY:SIDE//DIPLAYCOLOR//REFCOLOR//REFERENCEVALUE//STEPSIZE//MODE//BRIGHTNESS//URL//PATHXML//PATHJSON        
def addNewValueObject(side,displayColor,referenceColor,referenceValue,stepSize,mode,requestURL,pathOfValueXML,pathOfValueJSON):
    newValueObject= ValueHolder(side,displayColor,referenceColor,referenceValue,stepSize,mode,requestURL,pathOfValueXML,pathOfValueJSON)
    
    print "add new value object"

    if(side=='A'):
        clearSide("A")
        display.addNewValueObject(newValueObject,0)
    elif (side=='B'):
        clearSide("B")
        display.addNewValueObject(newValueObject,1)
    elif(side=='C'):
        clearSide("C")
        display.addNewValueObject(newValueObject,2)
    elif(side=='D'):
        clearSide("D")
        display.addNewValueObject(newValueObject,3)
        
def exitHandlerFunction():
   closeTcpConnection()

if __name__== '__main__':
    main()
