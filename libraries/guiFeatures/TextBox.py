'''Textbox feature'''

#import 3rd party libraries
import pygame

class TextBox():
    def __init__(self, window, width, height, x, y, showLineNumbers, startingText=""):
        self.window = window
        self.text = startingText
        self.width = width
        self.height = height
        self.x = x
        self.y= y
        self.showLineNumbers = showLineNumbers
        self.rect = pygame.Rect(x, y, width, height)

    def setFont(self, path):
        #load font
        self.font = pygame.font.Font(path)
    def update(self):
        mousePos = pygame.mouse.get_pos()
        pygame.draw.rect(self.window, (0, 0, 0), self.rect, 1)
        self.window.blit(self.wrapText(), self.rect)
        if (self.showLineNumbers):
            numLines = self.text.count("\n")
    def handleClick(self):
        mousePos = pygame.mouse.get_pos()
    def wrapText(self, width):
        pass
        