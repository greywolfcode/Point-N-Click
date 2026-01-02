#import standard libraries
import xml.etree.ElementTree

#import 3rd party libraries
import pygame

#import custom libraries
from guiFeatures.DropDown import DropDown
from guiFeatures.CheckBox import CheckBox
from guiFeatures.RadioButton import RadioButton


#initalise libraries
pygame.init()

#define window stuff
windowWidth = 800
windowHeight = 600

window = pygame.display.set_mode((windowWidth, windowHeight))

#define dictionarys to store map elemnts
mapElements = {
            "wall": {},
            "barrier": {},
}

#define class to store brushes
class Brush():
    def __init__(self, tag, continuous, xOffset):
        '''        
        tag: type of element
        continuous: creates over the range
        '''
        self.tag = tag
        self.continuous = continuous
        self.xOffset = xOffset
        self.currentlyDrawing = False
    def onClick(self):
        if editorWindow.mouseInWindow():
            if editorWindow.getSnapToGrid():
                startPos = editorWindow.getClickedCell()
            else:
                startPos = pygame.mouse.get_pos()
                startPos = pygame.Rect(startPos[0], startPos[1], 0, 0) #rect has no width or height
            self.startPos = pygame.Rect(startPos.x + self.xOffset, startPos.y, startPos.width, startPos.height)
            self.currentlyDrawing = True
    def onUnclick(self):
        if self.currentlyDrawing:
            if editorWindow.getSnapToGrid():
                endPos = editorWindow.getClickedCell().left
            else:
                endPos = pygame.mouse.get_pos()
                endPos = pygame.Rect(endPos[0], endPos[1], 0, 0) #rect has no width or height
            self.endPos = pygame.Rect(endPos.x + self.xOffset, endPos.y, endPos.width, endPos.height)
            #compile data
            data = {
                "xStart": self.startPos[0],
                "yStart": self.startPos[1],
                "xEnd": self.endPos[0],
                "yEnd": self.endPos[1],
            }
            #get name
            elementName = self.tag + " " + str(len(mapElements))
            #write basic data to map
            mapElements[elementName] = data
            self.currentlyDrawing = False
    def update(self):
        if self.currentlyDrawing:
            if editorWindow.getSnapToGrid():
                currentPos = editorWindow.getClickedCell()
            else:
                currentPos = pygame.mouse.get_pos()
                currentPos = pygame.Rect(currentPos[0], currentPos[1], 0, 0) #rect has no width or height
            #get width and height
            width = abs(currentPos[0] - self.startPos[0] + self.xOffset)
            height = abs(self.startPos[1] - currentPos[1])
            #get required coordinents for x
            if self.startPos.x + self.xOffset < currentPos.x:
                x = self.startPos.x + self.xOffset - width
            elif self.startPos.x + self.xOffset >= currentPos.x:
                x = currentPos.x
            #get required coordinents for y
            if self.startPos.y <= currentPos.y:
                y = self.startPos.y
            elif self.startPos.y > currentPos.y:
                y = currentPos.y
            
            #draw rect
            rectValues = (x, y, width, height)
            pygame.draw.rect(window, (0, 155, 0, 100), rectValues)
#main GUI features
class SideBar():
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 200, 600)
        #list to store all gui elements in
        self.guiElements = []
        #define grid display check box
        self.displayGrid = CheckBox(window, 20, 15, True, 20, text="Show Grid")
        self.displayGrid.setCommand(lambda doGrid: (editorWindow.setDisplayGrid(doGrid)))
        self.displayGrid.setFont(r"fonts\ScienceGothic-VariableFont_CTRS,slnt,wdth,wght.ttf")
        self.guiElements.append(self.displayGrid)
        #define snap to grid check box
        self.snapToGrid = CheckBox(window, 20, 40, True, 20, text="Snap to Grid")
        self.snapToGrid.setCommand(lambda doSnap: (editorWindow.setSnapToGrid(doSnap)))
        self.snapToGrid.setFont(r"fonts\ScienceGothic-VariableFont_CTRS,slnt,wdth,wght.ttf")
        self.guiElements.append(self.snapToGrid)
        #define tools radio buttons
        self.tools = RadioButton(window, 20, 120, 10, 10, "Tools", ("wall", "barrier"), "wall")
        self.tools.setCommand(lambda tool: editorWindow.setTool(tool))
        self.tools.setFont(r"fonts\ScienceGothic-VariableFont_CTRS,slnt,wdth,wght.ttf")
        self.guiElements.append(self.tools)
        #define grid selection drop down
        self.gridSelection = DropDown(window, 20, 75, ("Small", "Medium", "Large"), "Medium",)
        self.gridSelection.setCommand(lambda size: (editorWindow.setGridSize(size)))
        self.gridSelection.setFont(r"fonts\ScienceGothic-VariableFont_CTRS,slnt,wdth,wght.ttf")
        self.guiElements.append(self.gridSelection)
        
    def update(self):
        pygame.draw.rect(window, (138, 89, 54), self.rect, 5)
        for element in self.guiElements:
            element.update()
    def handleClick(self):
        for element in self.guiElements:
            element.handleClick()


class EditorWindow():
    def __init__(self):
        self.bg = pygame.image.load(r"images\bg\bg.png")
        self.rect = self.bg.get_rect()
        self.rect.x = 200
        self.rect.y = 0
        self.gridType = "m"
        self.doDisplayGrid = True
        self.snapToGrid = True
        #define brushes
        self.brushes = {
            "wall": Brush("wall", True, self.rect.x),
            "barrier": Brush("wall", True, self.rect.x),
        }
        self.currentBrush = self.brushes["wall"]
        #define largest grid of rects
        self.smallGrid = {}
        for x in range(200, 800, 5):
            for y in range(0, 600, 5):
                self.smallGrid[(x, y)] = pygame.Rect((x, y), (5, 5))
        #define medium, grid of rects
        self.mediumGrid = {}
        for x in range(200, 800, 10):
            for y in range(0, 600, 10):
                self.mediumGrid[(x, y)] = pygame.Rect((x, y), (10, 10))
        #define large, grid of rects
        self.largeGrid = {}
        for x in range(200, 800, 20):
            for y in range(0, 600, 20):
                self.largeGrid[(x, y)] = pygame.Rect((x, y), (20, 20))
    def update(self):
        window.blit(self.bg, self.rect)
        if (self.doDisplayGrid):
            self.displayGrid()
        self.currentBrush.update()
    def onClick(self):
        self.currentBrush.onClick()
    def onUnClick(self):
        self.currentBrush.onUnclick()
    def displayGrid(self):
        if self.gridType == "l":
            for cell in self.largeGrid.values():
                pygame.draw.rect(window, (255, 255, 255), cell, 1)
        elif self.gridType == "m":
            for cell in self.mediumGrid.values():
                pygame.draw.rect(window, (255, 255, 255), cell, 1)
        elif self.gridType == "s":
            for cell in self.smallGrid.values():
                pygame.draw.rect(window, (255, 255, 255), cell, 1)
    def setGridSize(self, size):
        if size == "Small":
            self.gridType = "s"
        elif size == "Medium":
            self.gridType = "m"
        elif size == "Large":
            self.gridType = "l"
    def setDisplayGrid(self, doDisplayGrid):
        self.doDisplayGrid = doDisplayGrid
    def setSnapToGrid(self, snapToGrid):
        self.snapToGrid = snapToGrid
    def getSnapToGrid(self):
        return self.snapToGrid
    def mouseInWindow(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    def setTool(self, tool):
        self.currentBrush = self.brushes[tool]
    def getClickedCell(self):
        '''Returns the cell that the mouse is in'''
        mousePos = pygame.mouse.get_pos()
        #get the current grid
        if self.gridType == "l":
            grid = self.largeGrid
        elif self.gridType == "m":
            grid = self.mediumGrid
        elif self.gridType == "s":
            grid = self.smallGrid
        #iterate through cells and find which was clicked
        for cell in grid.values():
            if cell.collidepoint(mousePos):
                return cell

#define objects
editorWindow = EditorWindow()
sideBar = SideBar()

#main loop
run = True
while run:
    #fill background
    window.fill((158, 109, 74))
    #update objects
    editorWindow.update()
    sideBar.update()
    #event handeler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            sideBar.handleClick()
            editorWindow.onClick()
        elif event.type == pygame.MOUSEBUTTONUP:
            editorWindow.onUnClick()
    
    #update display
    pygame.display.update()
#close pygame stuff
pygame.quit()