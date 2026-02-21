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
        self.text = [] #storing stings in list for efficiency
        self.selected = False;
    def setFont(self, path):
        #load font
        self.font = pygame.font.Font(path)
        self.textRender = self.font.render("", True, (0, 0, 0));
    def update(self):
        pygame.draw.rect(self.window, (0, 0, 0), self.rect, 1)
        self.window.blit(self.wrapText(), self.rect)
        self.window.blit(self.textRender, self.rect)
    def handleClick(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            self.selected = True
    def handleKey(self, event):
        if event.key == pygame.key.K_BACKSPACE:
            self.text.pop()
        elif event.key == pygame.key.K_RETURN:
            self.text.append("\n")
        else:
            self.text.append(event.unicode)
    def handleTextInput(self, event):
        self.text.extend(list(event))
    def renderText(self):
        width = self.window.length
        if (self.showLineNumbers):
            numLines = self.text.count("\n")
            lineNumLength = self.font.size(str(numLines) + 1)
            width -= lineNumLength

            lineNumString = []
            for num in range(0, numLines):
                lineNumString.extend([str(num), "\n"])
            
            lineNumRender = self.font.render("".join(lineNumString), True, (0, 0, 0)) #will fit length of line numbers, so doesn't require wrap
            textRender = self.font.render("".join(self.text), True, (0, 0, 0), wraplength=width)

            textSurface = pygame.Surface((self.window.width, lineNumRender.height))
            textSurface.blit(lineNumRender, (0, 0))
            textSurface.blit(textRender, (lineNumLength, 0))

            self.textRender = textSurface

        else:
            self.textRender = self.font.render("".join(self.text), True, (0, 0, 0), wraplength=width)