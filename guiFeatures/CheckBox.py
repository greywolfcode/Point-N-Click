'''Checkbox GUI feature'''

#import 3rd party libraries
import pygame

class CheckBox():
    def __init__(self, window, x, y, default, sideLength, text=""):
        self.window = window
        self.state = default
        self.text = text
        #define surfaces and rects
        self.surface = pygame.Surface((sideLength, sideLength))
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        #colour surface based on starting state
        if (self.state):
            self.surface.fill((0, 155, 0))
        else:
            self.surface.fill((0, 0, 0))
    def setCommand(self, command):
        self.command = command
    def setFont(self, path):
        self.font = pygame.font.Font(path)
        self.renderdText = self.font.render(self.text, True, (255, 255, 255))
    def update(self):
        self.window.blit(self.surface, self.rect)
        self.window.blit(self.renderdText, (self.rect.right, self.rect.top - 2))
    def handleClick(self):
        if (self.rect.collidepoint(pygame.mouse.get_pos())):
            self.state = not self.state
            self.command(self.state)
            #recolour surface
            if (self.state):
                self.surface.fill((0, 155, 0))
            else:
                self.surface.fill((0, 0, 0))