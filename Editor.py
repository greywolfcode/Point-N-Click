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
    def __init__(self, tag, continuous, xOffset, surface):
        '''        
        tag: type of element
        continuous: creates over the range
        '''
        self.tag = tag
        self.continuous = continuous
        self.xOffset = xOffset
        self.currentlyDrawing = False
        self.surface = surface
    def onClick(self):
        if editorWindow.mouseInWindow():
            if editorWindow.getSnapToGrid():
                startPos = editorWindow.getClickedCell()
            else:
                startPos = pygame.mouse.get_pos()
                startPos = pygame.Rect(startPos[0] - self.xOffset, startPos[1], 0, 0) #rect has no width or height
            self.startPos = pygame.Rect(startPos.x, startPos.y, startPos.width, startPos.height)
            self.currentlyDrawing = True
    def onUnclick(self):
        if self.currentlyDrawing:
            if editorWindow.getSnapToGrid():
                endPos = editorWindow.getClickedCell()
                endPos = pygame.Rect(endPos.right, endPos.bottom, 0, 0)
            else:
                endPos = pygame.mouse.get_pos()
                endPos = pygame.Rect(endPos[0] - self.xOffset, endPos[1], 0, 0) #rect has no width or height
            #get required coordinents for x
            if self.startPos.x < endPos.x:
                x = self.startPos.x
            elif self.startPos.x >= endPos.x:
                x = endPos.x
            #get required coordinents for y
            if self.startPos.y <= endPos.y:
                y = self.startPos.y
            elif self.startPos.y > endPos.y:
                y = endPos.y
            #get width and height
            width = abs(endPos[0] - self.startPos[0])
            height = abs(self.startPos[1] - endPos[1])
            data = {
                "x": x,
                "y": y,
                "width": width,
                "height": height,
            }
            #get name
            elementName = self.tag + " " + str(len(mapElements[self.tag]))
            #write basic data to map
            mapElements[self.tag][elementName] = data
            self.currentlyDrawing = False
    def update(self):
        if self.currentlyDrawing:
            if editorWindow.getSnapToGrid():
                currentPos = editorWindow.getClickedCell()
                currentPos = pygame.Rect(currentPos.right, currentPos.bottom, 0, 0)
            else:
                currentPos = pygame.mouse.get_pos()
                currentPos = pygame.Rect(currentPos[0] - self.xOffset, currentPos[1], 0, 0) #rect has no width or height
            #get width and height
            width = abs(currentPos[0] - self.startPos[0])
            height = abs(self.startPos[1] - currentPos[1])
            print(currentPos)
            #get required coordinents for x
            if self.startPos.x < currentPos.x:
                x = self.startPos.x
            elif self.startPos.x >= currentPos.x:
                x = currentPos.x
            #get required coordinents for y
            if self.startPos.y <= currentPos.y:
                y = self.startPos.y
            elif self.startPos.y > currentPos.y:
                y = currentPos.y
            
            #draw rect
            rectValues = (x, y, width, height)
            pygame.draw.rect(self.surface, (0, 155, 0, 100), rectValues)
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
        self.surface = pygame.image.load(r"images\bg\bg.png")
        self.rect = self.bg.get_rect()
        self.rect.x = 200
        self.rect.y = 0
        self.window = pygame.Surface
        self.gridType = "m"
        self.doDisplayGrid = True
        self.snapToGrid = True
        #define brushes
        self.brushes = {
            "wall": Brush("wall", True, self.rect.x, self.surface),
            "barrier": Brush("barrier", True, self.rect.x, self.surface),
        }
        self.currentBrush = self.brushes["wall"]
        #get bg images
        self.bgImages = {
            "wall": pygame.image.load(r"images\bg\wall_texture.png"),
            "barrier": pygame.image.load(r"images\bg\border_texture.png"),
        }
        #define largest grid of rects
        self.smallGrid = {}
        for x in range(0, 600, 5):
            for y in range(0, 600, 5):
                self.smallGrid[(x, y)] = pygame.Rect((x, y), (5, 5))
        #define medium, grid of rects
        self.mediumGrid = {}
        for x in range(0, 600, 10):
            for y in range(0, 600, 10):
                self.mediumGrid[(x, y)] = pygame.Rect((x, y), (10, 10))
        #define large, grid of rects
        self.largeGrid = {}
        for x in range(0, 600, 20):
            for y in range(0, 600, 20):
                self.largeGrid[(x, y)] = pygame.Rect((x, y), (20, 20))
        #defien frame stuff
        self.frame = 0
        self.frameCounter = 0
    def update(self):
        #reset surface
        self.surface.blit(self.bg, (0, 0))
        #update frame for border walls
        if self.frameCounter >= 50:
            self.frame += 1
            self.frameCounter = 0
        else:
            #TODO: Add frame rate independence?
            self.frameCounter += 1
        if self.frame > 15:
            self.frame = 0
        #draw all elements already placed
        for elementType in mapElements:
            for element in mapElements[elementType]:
                data = mapElements[elementType][element]
                coords = [data["x"], data["y"], data["width"], data["height"]]
                rect = pygame.Rect(coords)
                if elementType == "wall":
                    self.surface.blit(self.bgImages[elementType], rect, coords)
                elif elementType == "barrier":
                    coords[1] += 600 * self.frame
                    self.surface.blit(self.bgImages[elementType], rect, coords)
        if (self.doDisplayGrid):
            self.displayGrid()
        self.currentBrush.update()
        window.blit(self.surface, self.rect)
    def onClick(self):
        self.currentBrush.onClick()
    def onUnClick(self):
        self.currentBrush.onUnclick()
    def displayGrid(self):
        if self.gridType == "l":
            for cell in self.largeGrid.values():
                pygame.draw.rect(self.surface, (255, 255, 255), cell, 1)
        elif self.gridType == "m":
            for cell in self.mediumGrid.values():
                pygame.draw.rect(self.surface, (255, 255, 255), cell, 1)
        elif self.gridType == "s":
            for cell in self.smallGrid.values():
                pygame.draw.rect(self.surface, (255, 255, 255), cell, 1)
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
        adjustedPos = (mousePos[0] - self.rect.x, mousePos[1])
        #get the current grid
        if self.gridType == "l":
            grid = self.largeGrid
        elif self.gridType == "m":
            grid = self.mediumGrid
        elif self.gridType == "s":
            grid = self.smallGrid
        #iterate through cells and find which was clicked
        for cell in grid.values():
            if cell.collidepoint(adjustedPos):
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