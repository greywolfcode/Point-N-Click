'''GUI Radio Button feature'''

#import 3rd party libraries
import pygame

class RadioButton():
    def __init__(self, window, x, y, width, height, titleText, options, default):
        self.window = window
        self.titleText = titleText
        self.options = options
        self.currentOption = default
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = width / 2
        self.optionRects = {}
        
    def setCommand(self, command):
        self.command = command
    def setFont(self, path):
        #load font
        self.font = pygame.font.Font(path)
        self.titleRender = self.font.render(self.titleText, True, (255, 255, 255))
        self.defineRects()
    def defineRects(self):
        #create indivdual rects; not in constructor so font size can be used
        for index, option in enumerate(self.options):
            self.optionRects[option] = (pygame.Rect((self.x, self.y + 5 + self.font.size("random text")[1] +  (self.height * index)), ((self.width, self.height))))
    def update(self):
        self.window.blit(self.titleRender, (self.x, self.y))
        for option in self.options:
            if option == self.currentOption:
                pygame.draw.circle(self.window, (0, 155, 0), self.optionRects[option].center, self.radius)
            else:
                pygame.draw.circle(self.window, (1, 1, 1), self.optionRects[option].center, self.radius)
            self.window.blit(self.font.render(option, True, (255, 255, 255)), (self.optionRects[option].right, self.optionRects[option].y - self.optionRects[option].height))
    def handleClick(self):
        mousePos = pygame.mouse.get_pos()
        for option in self.optionRects:
            if self.optionRects[option].collidepoint(mousePos):
                self.currentOption = option
                self.command(self.currentOption)
                break
        