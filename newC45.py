import math
import pdb
import html.parser
import xml.dom.minidom

class MyHTMLParser( html.parser.HTMLParser):
    categoryValues = {}
    currentCategory = ""
    firstTime = True;
    listOfPairs = []
    def handle_starttag(self, tag, attrs):
        if (tag == 'variable'):            
            for (name, category )in attrs:
                if(self.firstTime == True ):
                    self.currentCategory = category;
                else:
                    self.currentCategory = category;
                    self.listOfPairs = []                                                                                                                                                  
        elif(tag == 'group'):
                listOfAttributes = []               
                for (name, groupName )in attrs:
                    listOfAttributes.append(groupName)                                                          
                pairValues = (listOfAttributes[0],listOfAttributes[1])            
                self.categoryValues[self.currentCategory] = self.listOfPairs             
                self.listOfPairs.append(pairValues)
        elif(tag == 'category'):
            for (name, category )in attrs:
                if(self.firstTime == True ):
                    self.currentCategory = category;
                else:
                    self.currentCategory = category;
                    self.listOfPairs = []
        elif(tag == 'choice'):
                listOfAttributes = []               
                for (name, groupName )in attrs:
                    listOfAttributes.append(groupName)                                                          
                pairValues = (listOfAttributes[0],listOfAttributes[1])            
                self.categoryValues[self.currentCategory] = self.listOfPairs             
                self.listOfPairs.append(pairValues) 
                              
        self.firstTime = False;                                                   

class Node:
    def __init__(self, isLeaf, label, threshold):
        self.label = label
        self.threshold = threshold
        self.isLeaf = isLeaf
        self.children = []

class C45:
    def __init__(self, data, names):
        self.data = data
        self.names = names
        self.avals = {}
        self.att = []
        self.items = []
        self.classes = []
        self.atts = -1
        self.tree = None

    def fetcher(self):       
        with open(self.names, "r") as file:
            parser = MyHTMLParser()
            #HTML Parser            
            for line in file:
                parser.feed(line) 
            
            classAttributes = []
                           
            for key in parser.categoryValues.keys():
                print (key)
                print(parser.categoryValues[key])
            for attributeKey in parser.categoryValues.keys():
                values = []
                for pairs in parser.categoryValues[attributeKey]:
                    values.append(pairs[0])
                    classAttributes.append(pairs[0])
                self.avals[attributeKey] = values 
                               
        #self.classes = classAttributes
        self.classes = list(parser.categoryValues.keys())
        self.atts = len(self.avals.keys())
        self.att = list(self.avals.keys())       
        lineCount = 0
        
        print(self.classes)
        
        with open(self.data, "r") as file:
            for line in file:
                lineCount += 1
                if(lineCount > 3):
                    row = [x.strip()  for x in line.split(",")]
                    if row != [] or row != [""]:
                        print(row)
                        self.items.append(row)
    def calculateEntropyD(self, items):
        obamaCount = 0
        mccainCount = 0
        print('lengthofitems')
        print(len(items))
        if(len(items) == 0):
            return 0
        print('items')
        print(items)
        for item in items:
            if(item[11] == 'Obama'):
                obamaCount += 1
            elif(item[11] == 'McCain'):
                mccainCount += 1
        print('oCount')
        print(obamaCount)
        print('mccainCount')
        print(mccainCount)
        obamaPR = obamaCount/(float(len(items)))
        mccainPR =  mccainCount/ (float(len(items)))
        
        print('obamaPR')
        print(obamaPR)
        print('mccainPR')
        print(mccainPR)
        
        if(obamaCount == 0 or mccainCount == 0):
            return 0

        entropy = (-(obamaPR) * math.log2(obamaPR)) - ((mccainPR) * math.log2(mccainPR))
        
        return entropy
    def getListOfSlices(self, currentClassIndex, classValues, items):
        listOfSlices = list()
        classValuesLen = len(classValues)
        for i in range(0, classValuesLen):
            listOfSlices.append([])
         
        for i in range(0,classValuesLen):  
            for item in items:        
                    if(item[currentClassIndex + 1] == classValues[i]):
                        sliceList = listOfSlices[i]
                        sliceList.append(item)
                        listOfSlices[i] = sliceList 
                                            
        
        return listOfSlices                        
    def calculateEntropyAI(self,listOfSlices,items):         
        totalAmountOfItems = len(items) 
        totalEntropy = 0       
        entropies = []
                
        for sliceList in listOfSlices:
            entropy = self.calculateEntropyD(sliceList)
            print('entropy')
            print(entropy)
            entropies.append(entropy)
                
        entropyIndex = 0
        for entropy in entropies:
            sliceLen = len(listOfSlices[entropyIndex])                   
            sliceListEntrophy = entropy * (float(sliceLen)/ float(totalAmountOfItems))
            print('slice')
            print(sliceListEntrophy)
            totalEntropy += sliceListEntrophy  
            entropyIndex += 1  
        
        print('total entrophy')
        print(totalEntropy)
        
        return totalEntropy  
        
    def homogeneousCheck(self,items):

        if(len(items) == 0):
            return False                
        homoCheck = items[0][11]
        print('homo')
        print(homoCheck)
        
        for item in items:
            if(item[11] != homoCheck):
                return False
        return True
               
    def splitter(self, items, excludedClasses):
        
        if(self.homogeneousCheck(items)):
            items[0][11]
            print('decision : ' + items[0][11])
            
        classIndex = 0
        entropyD = self.calculateEntropyD(self.items) 
        print("topLevel EntropyD")
        print(entropyD)
        maxAttributeIndex = 0
        maxAttribute = ""
        maxGain = 0.0             
        for i in range(0, self.classes.__len__() - 1):
            print('currentClass')
            print(self.classes[i])
            currentClass = self.classes[i]
            currentClassIndex = i
            
            classValues = self.avals[currentClass]
            listOfSlices = self.getListOfSlices(currentClassIndex, classValues, items)
            print('list of slices')
            print(listOfSlices)
            totalEntropy = self.calculateEntropyAI(listOfSlices,items)
            
            informationGain = entropyD - totalEntropy
            print('information gain')
            print(informationGain)
            
            if(informationGain > maxGain):
                maxAttributeIndex = i
                maxAttribute = self.classes[maxAttributeIndex]
                maxGain = informationGain            

        excludedClasses[maxAttributeIndex] = True
        
        print('firstrun')
        print(maxAttribute)
        print(maxGain)
                   
    def processData(self):
        excludedClasses = {}       
        self.splitter(self.items,excludedClasses)

if __name__ == "__main__":
    c = C45("tree03/tree03-20-words.csv", "domain.xml")
    c.fetcher()
    c.processData()
    