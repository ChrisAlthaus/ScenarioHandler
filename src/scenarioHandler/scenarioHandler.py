from valueHolder import *
from messageHandler import *
from displayHandler import *
import time

from subprocess import check_output


spi= None

            
display=displayHandler(10)

addSubValue=0

def main():
    init_spi()
    
    #if isWifiConnected() is False:
    #    showWifiConnectionError()
    #    return
    
    display.displayData()
   
    
    message="DISPLAY:C//3FE71A//FFFFFF//10//5//FROMBOTTOMTOTOP"
    message+="//api.openweathermap.org/data/2.5over&APPID=d1e9d70bdb58b701b0366495d128403d&mode=xml"
    message+="//temperature,value//None"
    
    parseMessage(message)
   
    message="DISPLAY:A//3FE71A//FFFFFF//273//5//FROMBOTTOMTOTOP"
    message+="//api.openweathermap.org/data/2.5over&APPID=d1e9d70bdb58b701b0366495d128403d&mode=xml"
    message+="//temperature,value//None"
    
    #parseMessage(message)
    
    message="DISPLAY:B//2347d7//b1b6b1//0//12//FROMBOTTOMTOTOP"
    message+="//api.openweathermap.org/data/2.5/weather?q=Hannover&APPID=d1e9d70bdb58b701b0366495d128403d"
    message+="//None//main,humidity"
    
    #parseMessage(message)
    
    
    
def isWifiConnected():
    wifi_ip = check_output(['ifconfig', '$wlan | grep -q "inet addr:"'])
    if wifi_ip is None:
        return False
    else:
        return True  
    

        
def showWifiConnectionError(self):
   setSingleAnimation("PULSESLOW", self.side, NUMBER_LEDS, 10000, colors['red'])  #show warning, if url unreachable      

#DISPLAY:SIDE//DIPLAYCOLOR//REFCOLOR//REFERENCEVALUE//STEPSIZE//MODE//BRIGHTNESS//URL//PATHXML//PATHJSON    #TODO: RANGEMAPPING

#TEMPERATURE:TIME//CITY//COUNTRY//BARSIDE//BRIGHTNESS
#RAIN:TIME//CITY//COUNTRY//BARSIDE//BRIGHTNESS


def parseMessage(message):
    print("Parsing message")  #log file
    messageLength= len(message)
    seperatorIndex=message.index(':')
    
    mode= message[0:seperatorIndex]
    
    values= message[seperatorIndex+1:messageLength]
    values = values.split("//")
    
    
    side=values[0]
    displayColor=values[1]
    referenceColor=values[2]
    referenceValue=float(values[3])
    stepSize=float(values[4])
    mode=values[5]
    
    requestURL=values[6]

    
    pathXML=None
    pathJson=None
    
    if(values[7] != "None"):
        pathXML=values[7].split(",")
    if(values[8] != "None"):
        pathJson=values[8].split(",")
          
    
    if(pathJson is None):
        addNewValueObject(side,displayColor,referenceColor,referenceValue,stepSize,mode,requestURL,pathXML,None)
    elif(pathXML is None):
        addNewValueObject(side,displayColor,referenceColor,referenceValue,stepSize,mode,requestURL,None,pathJson)
    else:
        print("No SearchPath.") #error log
    
    print(values)

def scaleValue(value): #scale value, e.g. distribution,intervalls
    
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
        


if __name__== '__main__':
    main()
