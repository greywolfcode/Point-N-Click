#import standard libraries

#import 3rd party libraries
import pygame

#import custom libraries
from guiFeatures.DropDown import DropDown

#initalise libraries
pygame.init()

#define window stuff
windowWidth = 800
windowHeight = 600

window = pygame.display.set_mode((windowWidth, windowHeight))
#GUI component classes

#main GUI features
class SideBar():
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 200, 600)
        
        self.gridSelection = DropDown(window, ("Small", "Medium", "Large"), "Large", 10, 10)
        self.gridSelection.setCommand(lambda size: (editorWindow.setGridSize(size)))
    def update(self):
        pygame.draw.rect(window, (138, 89, 54), self.rect, 5)
        self.gridSelection.update()
    def handleClick(self):
        self.gridSelection.handleClick()
    
class EditorWindow():
    def __init__(self):
        self.bg = pygame.image.load(r"images\bg\bg.png")
        self.rect = self.bg.get_rect()
        self.rect.x = 200
        self.rect.y = 0
        self.gridType = "m"
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
        self.displayGrid()
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
    
    #update display
    pygame.display.update()
#close pygame stuff
pygame.quit()