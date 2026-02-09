import xml.etree.ElementTree as ET
from xml.sax import parse
from xml.sax import ContentHandler


class LayoutParser(ContentHandler):
    def __init__(self):
        self.elements = {}
        self.currentGroup = ""
        self.currentElement = ""
        self.currentData = ""
        self.currentType = ""
    #overloaded methods to handle data
    def startElement(self, name, attrs):
        if len(attrs) == 0: #catch for sections without a type
            return
        if attrs["type"] == "group":
            self.elements[name] = {}
            self.currentGroup = name
        elif attrs["type"] == "element":
            self.elements[self.currentGroup][name] = {}
            self.currentElement = name
        else:
            self.currentData = name
            self.currentType = attrs["type"]
    def characters(self, content):
        if self.currentType == "int":
            self.elements[self.currentGroup][self.currentElement][self.currentData] = int(content)
        elif self.currentType == "str":
            self.elements[self.currentGroup][self.currentElement][self.currentData] = content
    def getElements(self):
        return self.elements


def saveLevelLayout(levelStructure, fileName):
    #create xml element
    root = ET.Element("levelData")
    #loop through all types of elements
    for elementType in levelStructure:
        typeElement = ET.SubElement(root, elementType)
        #add label attributes
        typeElement.set("type", "group")
        #loop through all elements
        for element in levelStructure[elementType]:
            elementElement = ET.SubElement(typeElement, element)
            #add label attributes
            elementElement.set("type", "element")
            #loop through all attributes of elements
            for attribute in levelStructure[elementType][element]:
                dataElement = ET.SubElement(elementElement, attribute)
                dataElement.set("type", type(levelStructure[elementType][element][attribute]).__name__)
                dataElement.text = str(levelStructure[elementType][element][attribute])

    data = ET.tostring(root)

    #save file
    with open("layout.xml", "wb") as file:
        file.write(data)

def loadLevelLayout(filePath):
    #create parsing object
    parser = LayoutParser()
    #parse file
    parse(filePath, parser)
    #return elements as dictionary
    return parser.getElements()