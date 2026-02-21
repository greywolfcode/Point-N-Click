'''Textbox feature'''

#import 3rd party libraries
import pygame

class TextBox():
    def __init__(self, window, x, y, showLineNumbers=False, startingText="", width="any", height="any"):
        self.window = window
        self.text = startingText

        if (width == "any"):
            self.width = window.width
        else:
            self.width = width

        if (height == "any"):
            self.height = window.height
        else:
            self.height = height

        self.x = x
        self.y= y
        self.showLineNumbers = showLineNumbers
        self.rect = pygame.Rect((x, y), (self.width, self.height))
        self.text = [] #storing stings in list for efficiency
        self.selected = False
    def setFont(self, path):
        #load font
        self.font = pygame.font.Font(path)
        self.renderText()
    def update(self):
        pygame.draw.rect(self.window, (0, 0, 0), self.rect, 1)
        self.window.blit(self.textRender, self.rect)
    def handleClick(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            self.selected = True
    def handleKey(self, event):
        '''For pygame.event.key'''
        if event.key == pygame.K_BACKSPACE and len(self.text) > 0:
            self.text.pop()
        elif event.key == pygame.K_RETURN:
            self.text.append("\n")
        else:
            self.text.append(event.unicode)
        self.renderText()
    def handleTextInput(self, event):
        '''For pygame.event.text'''
        self.text.extend(list(event.text))
        self.renderText()
    def renderText(self):
        width = self.width
        if (self.showLineNumbers):
            numLines = self.text.count("\n")
            lineNumLength = self.font.size(str(numLines) + " ")[0]
            width -= lineNumLength

            lineNumString = []
            for num in range(0, numLines+1):
                lineNumString.extend([str(num+1), " \n"])
            
            lineNumRender = self.font.render("".join(lineNumString), True, (0, 0, 0)) #will fit length of line numbers, so doesn't require wrap
            textRender = self.font.render("".join(self.text), True, (0, 0, 0), wraplength=width)

            textSurface = pygame.Surface((self.window.width, self.height), pygame.SRCALPHA)
            textSurface.fill((0, 0, 0, 0))
            textSurface.blit(lineNumRender, (0, 0))
            textSurface.blit(textRender, (lineNumLength, 0))

            self.textRender = textSurface
        else:
            self.textRender = self.font.render("".join(self.text), True, (0, 0, 0), wraplength=width)