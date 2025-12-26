'''Drop down option selection box'''

#import 3rd party libraries
import pygame

class DropDown():
    def __init__(self, window, options, default, x, y, closeOnClick=True):
        self.window = window
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
        self.openRect.y = self.closedRect.bottom
        self.openRects = {}
        for i, option in enumerate(self.options):
            self.openRects[option] = pygame.Rect((0, (50*i)), (100, 50))
    def setFont(self, path):
        #load font
        self.font = pygame.font.Font(path)
    def setCommand(self, command):
        self.command = command
    def update(self):
        self.closed.fill((138, 89, 54))
        self.closed.blit(self.font.render(self.currentOption, True, (255, 255, 255)), (0, 0))
        self.window.blit(self.closed, self.closedRect)
        if self.isOpen:
            self.open.fill((128, 79, 44))
            #draw options 
            for option in self.options:
                self.open.blit(self.font.render(option, True, (255, 255, 255)), self.openRects[option])
                pygame.draw.rect(self.open, (0, 0, 0), self.openRects[option], 1)
            self.window.blit(self.open, self.openRect)
    def handleClick(self):
        if self.closedRect.collidepoint(pygame.mouse.get_pos()):
            self.isOpen = not self.isOpen
            return
        #modify mouse pos so it works with relitive position with dropdown
        mousePos = pygame.mouse.get_pos()
        realativeMousePos = (mousePos[0] - self.openRect.x, mousePos[1] - self.openRect.y)
        for option in self.openRects:
            if self.openRects[option].collidepoint(realativeMousePos):
                #run command with option
                self.command(option)
                #set new current option and close dropdown
                self.currentOption = option
                if self.closeOnClick:
                    self.isOpen = False
                break