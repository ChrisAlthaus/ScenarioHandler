import threading

            
class displayHandler():
    
    displays=[None]*4   
    #testValues=[40,45,50,55,60,70,20,30,40]
    #index=0
    
    def __init__(self,delay):
        self.delay=delay    #delay in seconds
        
        
    def displayData(self):
        print("display data")
        for i in range(0,4):
                if(self.displays[i] is not None):
                    print "side=", self.displays[i].side
                    self.displays[i].printValueHolder()
                    self.displays[i].setValue()
                    #self.displays[i].value=self.testValues[self.index]
                    #self.index= self.index + 1
                    #self.displays[i].displayFromBottomToTopMovingHeight()
                    self.displays[i].display()
                    print("value=",self.displays[i].value)
        
        nextCall =threading.Timer(self.delay,self.displayData)
        nextCall.start()
        
     
    def addNewValueObject(self,newValueObject,index):
        self.displays[index]= newValueObject
        
   
