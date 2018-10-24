import math
import pdb
import html.parser
import xml.dom.minidom
from platform import node

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
    def __init__(self, data, names,document):
        self.data = data
        self.names = names
        self.avals = {}
        self.att = []
        self.items = []
        self.classes = []
        self.atts = -1
        self.tree = None
        self.xmlDoc = document
        self.currentSelection = ""
        self.decisionClassIndex = 0

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
        self.decisionClassIndex = len(self.classes) -1
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
        setosaCount = 0
        versicolorCount = 0
        virginicaCount = 0
        areZeroes = 0
        entropy = 0
        if(len(items) == 0):
            return 0
        #print(items)
        for item in items:
            if(item[self.decisionClassIndex] == 'Iris-setosa'):
                setosaCount += 1
            elif(item[self.decisionClassIndex] == 'Iris-versicolor'):
                versicolorCount += 1
            else:
                virginicaCount += 1

        setosaPR = setosaCount/(float(len(items)))
        versicolorPR =  versicolorCount/ (float(len(items)))
        virginicaPR = virginicaCount/ (float(len(items)))
        
        if(versicolorCount == 0):
            areZeroes += 1
        if(virginicaCount == 0):
            areZeroes +=1
        if(setosaCount == 0):
            areZeroes += 1
          
        if(areZeroes >= 2):
            return 0;      
        elif(setosaCount == 0):
            entropy =  - ((versicolorPR) * math.log2(versicolorPR)) - ((virginicaPR) * math.log2(virginicaPR))
        elif(versicolorCount == 0):
            entropy =   - ((virginicaPR) * math.log2(virginicaPR)) - ((setosaPR) * math.log2(setosaPR)) 
        elif(virginicaCount == 0):
            (-(setosaPR) * math.log2(setosaPR)) - ((versicolorPR) * math.log2(versicolorPR))
        else:
            entropy = (-(setosaPR) * math.log2(setosaPR)) - ((versicolorPR) * math.log2(versicolorPR)) - ((virginicaPR) * math.log2(virginicaPR))
  
        return entropy
    def getNumericalSlices(self,currentClassIndex,items,entropyD):
        listOfSlices = list()
        bestGain = 0;
        bestList1 = list()
        bestList2 = list()
        sortedList = list()
        valueSplitOn = 0;
        
        sortedList = sorted(items , key=lambda x: x[currentClassIndex])
        print('sorted')
        print(currentClassIndex)
        print(sortedList)
        
        for i in range(1, len(items)):
            splitList1 = sortedList[:i]
            splitList2 = sortedList[i:]
            
            entropy1 = self.calculateEntropyD(splitList1)
            entropy2 = self.calculateEntropyD(splitList2)
            
            totalEntropy = entropy1 * (len(splitList1)/len(items)) + entropy2 * (len(splitList2)/len(items))
            
            informationGain = entropyD - totalEntropy
            
            if(informationGain >= bestGain):
               bestGain = informationGain
               bestList1 = splitList1
               bestList2 = splitList2 
               
        valueSplitOn = bestList2[0]  
        listOfSlices.append(bestList1)
        listOfSlices.append(bestList2)
        
        print('here')
        print(sortedList)
        print(valueSplitOn)
        floatSplitOn = valueSplitOn[currentClassIndex]  
        print('floatsplitOn')
        print(floatSplitOn)     
        
        return (listOfSlices,floatSplitOn)
                    
    def getListOfSlices(self, currentClassIndex, classValues, items):
        listOfSlices = list()
        classValuesLen = len(classValues)
        for i in range(0, classValuesLen ):
            listOfSlices.append([])
         
        for i in range(0,classValuesLen):  
            for item in items:        
                    if(item[currentClassIndex + 1] == classValues[i]):
                        sliceList = listOfSlices[i]
                        sliceList.append(item)
                        listOfSlices[i] = sliceList 
                                            
        
        return listOfSlices                        
    def calculateEntropyAI(self,listOfSlices,items): 
        print ('entropyAI')        
        totalAmountOfItems = len(items) 
        print(listOfSlices)
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
     
    def mostFrequentItems(self,items):   
        setosaCount = 0
        versicolorCount = 0
        virginicaCount = 0
        
        for item in items:
            if(item[self.decisionClassIndex] == 'Iris-setosa'):
                setosaCount += 1
            elif(item[self.decisionClassIndex] == 'Iris-versicolor'):
                versicolorCount += 1
            else:
                virginicaCount += 1
                
        if(setosaCount > versicolorCount and setosaCount > virginicaCount ):
            return 'Iris-setosa'
        elif (setosaCount < versicolorCount and virginicaCount < versicolorCount):
            return 'Iris-versicolor'
        elif(virginicaCount > versicolorCount and virginicaCount > setosaCount):
            return 'Iris-virginica'
        else:
            return "Neither"
        
    def homogeneousCheck(self,items):
        if(len(items) == 0):
            return False 
        print(self.decisionClassIndex)   
        print(items)            
        homoCheck = items[0][self.decisionClassIndex]
        print('homo')
        print(homoCheck)
        
        for item in items:
            if(item[self.decisionClassIndex] != homoCheck):
                return False
        return True
               
    def splitter(self, items, excludedClasses,node):
        
        if(self.homogeneousCheck(items)):
            print('Im Homo')
            print('decision : ' + items[0][self.decisionClassIndex])
            newNode = self.xmlDoc.createElement('decision')
            newNode.setAttribute('end', items[0][self.decisionClassIndex])
            node.appendChild(newNode)
        
        elif(len(excludedClasses) ==  len(self.classes)):
            print('decision :' + items[0][self.decisionClassIndex]) 
            newNode = self.xmlDoc.createElement('decision')
            newNode.setAttribute('end', items[0][self.decisionClassIndex])
            node.appendChild(newNode)
        elif(len(items) == 0):
            newNode = self.xmlDoc.createElement('decision')
            newNode.setAttribute('end', self.currentSelection)
            node.appendChild(newNode)                     
        else:
            self.currentSelection = items[0][self.decisionClassIndex]
            entropyD = self.calculateEntropyD(items) 
            print("topLevel EntropyD")
            print(entropyD)
            maxAttributeIndex = 0
            maxAttribute = ""
            maxGain = 0.0 
            maxListOfSlices = []
            classToSplitOn = " "
            maxValueSplitOn = 0.0
            
            print('items')
            print(items)          
            for i in range(0, self.classes.__len__() - 1):
                
                if( i not in excludedClasses):           
                    print('currentClass')
                    print(self.classes[i])
                    currentClass = self.classes[i]
                    currentClassIndex = i
                    
                    classValues = self.avals[currentClass]
                    print(len(classValues))
                    
                    if(len(classValues) > 1):                   
                        listOfSlices = self.getListOfSlices(currentClassIndex, classValues, items)
                        print('list of slices')
                        print(listOfSlices)
                        totalEntropy = self.calculateEntropyAI(listOfSlices,items)
                        
                        informationGain = entropyD - totalEntropy
                        print('information gain')
                        print(informationGain)
                        
                        if(informationGain > maxGain):
                            maxListOfSlices = listOfSlices
                            classToSplitOn = currentClass
                            maxAttributeIndex = i
                            maxAttribute = self.classes[maxAttributeIndex]
                            maxGain = informationGain   
                        excludedClasses[maxAttributeIndex] = True  
                    else:
                        print ("whe")
                        listOfSlices,valueSplitOn = self.getNumericalSlices(currentClassIndex,items, entropyD)
                        print('list')
                        print(listOfSlices)
                        print(valueSplitOn)
                        
                        totalEntropy = self.calculateEntropyAI(listOfSlices,items)
                        
                        informationGain = entropyD - totalEntropy
                        print('information gain')
                        print(informationGain)
                        
                        if(informationGain > maxGain):
                            maxListOfSlices = listOfSlices
                            classToSplitOn = currentClass
                            maxValueSplitOn = valueSplitOn
                            maxAttributeIndex = i
                            maxAttribute = self.classes[maxAttributeIndex]
                            maxGain = informationGain                       
                        
            
            ## If the algorithm cannot choose an attribute to split on
            if(classToSplitOn == " "):
                mostFrequentItem = self.mostFrequentItems(items)
                newNode = self.xmlDoc.createElement('decision')
                newNode.setAttribute('end', items[0][self.decisionClassIndex])
                node.appendChild(newNode)                       
            else:
                newNode = self.xmlDoc.createElement('node')
                newNode.setAttribute('var', classToSplitOn)
                node.appendChild(newNode)            
                                
                attributeIndex = 0
                classValues = self.avals[classToSplitOn]
           

                print('firstrun')
                print(maxAttribute)
                print(maxGain)
                

                print('listS')
                print(listOfSlices)       
                for list in maxListOfSlices:
                    edge = self.xmlDoc.createElement('edge')
                    print('classvalues')
                    print(classValues)
                    print(len(listOfSlices))  
                    print(attributeIndex)
                    if(len(classValues) > 1):                                      
                        edge.setAttribute('var ', classValues[attributeIndex])
                        edge.setAttribute('num', str(attributeIndex + 1))           
                        newNode.appendChild(edge)  
                        self.splitter(list, excludedClasses, edge) 
                        attributeIndex += 1 
                    else:
                        if(attributeIndex > 0):
                            edge.setAttribute('var ', 'GTE ' + str(maxValueSplitOn))                                    
                        else:                             
                            edge.setAttribute('var ', 'LT ' + str(maxValueSplitOn))   
                                                            
                    newNode.appendChild(edge)  
                    self.splitter(list, excludedClasses, edge) 
                    attributeIndex += 1                   
                         

                   
    def processData(self, node):
        excludedClasses = {}       
        self.splitter(self.items,excludedClasses,node) 
        
    def parseTree(self,node,item):
        trueValue = False
        equalTrigger = False
        endTrigger = False
        if(node.hasChildNodes()):
            for childnode in node.childNodes:
                attributes = childnode._get_attributes()
                for attribute in attributes.keys():
                    attributeString = str(attributes[attribute].value)
                    for class1 in self.classes:
                        if(class1.strip() == str(attributes[attribute].value).strip(" ")):
                            equalTrigger = True
    
                    if(equalTrigger == True):
                        attributeValue = attributes[attribute].value
                        indexValue = self.classes.index(attributeValue, 0, len(self.classes))
                        for edgeNode in childnode.childNodes:
                                                        
                            edgeAttributes = edgeNode._get_attributes()
                            splitArray = list()
                            for edgeAttribute in edgeAttributes.keys():
                                stringValue = edgeAttributes[edgeAttribute].value
                                splitArray = stringValue.split(" ")
                             
                            
                            if(splitArray[0] == 'LT'):
                                if(float(item[indexValue]) < float(splitArray[1])):
                                    testAttributes = edgeNode.firstChild._get_attributes()
                                    for testAttribute in testAttributes.keys():
                                        if(testAttribute == 'end'):
                                            endTrigger = True
                                        
                                    if(endTrigger):                                      
                                        trueValue= self.parseTree(edgeNode.firstChild,item)
                                    else:
                                        trueValue = self.parseTree(edgeNode,item)

                            elif(splitArray[0] == 'GTE'):
                                if(float(item[indexValue]) >= float(splitArray[1])):
                                    testAttributes = edgeNode.firstChild._get_attributes()
                                    for testAttribute in testAttributes.keys():
                                        if(testAttribute == 'end'):
                                            endTrigger = True
                                        
                                    if(endTrigger):                                      
                                        trueValue= self.parseTree(edgeNode.firstChild,item)
                                    else:
                                        trueValue = self.parseTree(edgeNode,item)
                                        
                                    
            return trueValue                
        else:
            nodeAttributes = node._get_attributes()            
            for attribute in nodeAttributes.values():
                if(item[self.decisionClassIndex] == attribute.value):
                    return True
                else:
                    return False
                      
                              
    def calculateAccuracy(self,node):

        accuracyCount = 0;
        currentNode = node  
        #self.parseTree(node, self.items[55])      
        for item in self.items:
            if(self.parseTree(node,item)):
                accuracyCount += 1
        print('accuracy')
        print(accuracyCount)
        print(float(accuracyCount)/float(len(self.items)))
           
if __name__ == "__main__":
    document = xml.dom.minidom.Document()
    node = document.createElement('Tree')
    node.setAttribute('known', "Something")
    document.appendChild(node)
    
    c = C45("iris/iris.data", "iris/domain.xml",document)
    c.fetcher()
    c.processData(node)
    print (document.toprettyxml())
    c.calculateAccuracy(node)
       
    
    