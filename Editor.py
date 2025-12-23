#import standard libraries

#import 3rd party libraries
import pygame

#initalise libraries
pygame.init()

#define window stuff
windowWidth = 800
windowHeight = 600

window = pygame.display.set_mode((windowWidth, windowHeight))
#GUI component classes
class DropDown():
    def __init__(self, command, options, default, x, y, closeOnClick=True):
        self.command = command
        self.options = options
        self.isOpen = False
        self.currentOption = default
        self.closeOnClick = closeOnClick
        #define surfaces and rects
        self.closed =  pygame.Surface((100, 50))
        self.closedRect = self.closed.get_rect()
        self.closedRect.x = x
        self.closedRect.y = y
        self.open = pygame.Surface((100, 50 * len(options)))
        self.openRect = self.open.get_rect()
        self.openRect.x = x
        self.openRect.y = self.closedRect.bottom + 10
        self.openRects = {}
        for i, option in enumerate(self.options):
            self.openRects[option] = pygame.Rect((0, 0 + (50*i)), (100, 50))
        #load font
        self.font = pygame.font.Font(r"fonts\ScienceGothic-VariableFont_CTRS,slnt,wdth,wght.ttf")

    def update(self):
        self.closed.fill((138, 89, 54))
        self.closed.blit(self.font.render(self.currentOption, True, (255, 255, 255)), self.closedRect)
        window.blit(self.closed, self.closedRect)
        if self.isOpen:
            self.open.fill((128, 79, 44))
            #draw options 
            for option in self.options:
                self.open.blit(self.font.render(option, True, (255, 255, 255)), self.openRects[option])
                pygame.draw.rect(self.open, (0, 0, 0), self.openRects[option], 1)
            window.blit(self.open, self.openRect)
    def handleClick(self):
        if self.closedRect.collidepoint(pygame.mouse.get_pos()):
            self.isOpen = not self.isOpen
            return
        for option in self.openRects:
            if self.openRects[option].collidepoint(pygame.mouse.get_pos()):
                print(8)
                #run command with option
                self.command(option)
                #set new current option and close dropdown
                self.currentOption = option
                if self.closeOnClick:
                    self.isOpen = False
                break
        
#main GUI features
class SideBar():
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 200, 600)
        
        self.gridSelection = DropDown(lambda size: (editorWindow.setGridSize(size)), ("Small", "Medium", "Large"), "Large", 10, 10)

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