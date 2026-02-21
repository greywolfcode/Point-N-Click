'''Scroll Bar feature'''

#import 3rd party libraries
import pygame

class ScrollBar():
    def __init__(self, window, side, scrollRect, scrollDirection, size):
        '''size is the width or height depending on location of scrollbar
            scrollDirection is horz or vert
        '''
        self.window = window
        self.side = side
        self.scrollRect = scrollRect
        self.scrollDirection = scrollDirection
        #figure out rect size based on surface to move and surface to render on
        if (self.scrollDirection == "horz"):
            self.width = window.width / scrollRect.width
            self.height = size
        elif (self.scrollDirection == "vert"):
            self.height = window.height / scrollRect.height
            self.width = size
        if (self.side == "left"):
            self.x = self.window.x
            self.y = self.window.y
        elif (self.side == "right"):
            self.x = self.window.right - self.width
            self.y = self.window.y = self.window.y
        elif (self.side == "top"):
            self.x = self.window.x
            self.y = self.window.top
        elif (self.side == "bottom"):
            self.x = self.window.left
            self.y = self.window.bottom - self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hover = False
    def update(self):
        mousePos = pygame.mouse.get_pos()
        if (self.rect.collide_point(mousePos)):
            self.hover = True
        else:
            self.hover = False
        if (self.hover):
            pygame.draw.rect(self.window, (50, 50, 50), self.rect, 1)
        else:
            pygame.draw.rect(self.window, (75, 75, 75), self.rect, 1)
    def handleClick(self):
        mousePos = pygame.mouse.get_pos()
        if (self.hover):
            self.rect.x = mousePos
        