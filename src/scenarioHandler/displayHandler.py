import threading
import copy
            
class displayHandler():
    
    displays=[None]*4   
    #testValues=[40,45,50,55,60,70,20,30,40]
    #index=0
    delay=40
   # def __init__(self,delay):
    #    self.delay=delay    #delay in seconds
    #TODO: copy display list to avoid NoneType error
    def changeDelay(self,delay):
	self.delay= delay    
        
    def displayData(self):
        print("display data")
        threadDisplays = copy.deepcopy(self.displays)

        for i in range(0,4):
                if(threadDisplays[i] is not None):
                    print "side=", threadDisplays[i].side
                    threadDisplays[i].printValueHolder()
                    threadDisplays[i].setValue()
                    #self.displays[i].value=self.testValues[self.index]
                    #self.index= self.index + 1
                    #self.displays[i].displayFromBottomToTopMovingHeight()
                    threadDisplays[i].display()
                    print("value=",threadDisplays[i].value)
        #print "delay=",self.delay
        nextCall =threading.Timer(self.delay,self.displayData)
        nextCall.start()
        
     
    def addNewValueObject(self,newValueObject,index):
        self.displays[index]= newValueObject
        
    def resetSide(self,index):
        self.displays[index]= None   
