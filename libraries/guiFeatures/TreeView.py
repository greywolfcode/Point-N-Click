'''GUI feature for viewing tree structures'''

#import 3rd party libraries
import pygame

class TreeView():
    def __init__(self, window, x, y, width, name):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.nodes = Node(None, name)
    def setFont(self, path):
        #load font
        self.font = pygame.font.Font(path)
        self.titleRender = self.font.render(self.titleText, True, (255, 255, 255))
        self.defineRects()
    def addNode(name, parentPath):
        pass

class Node():
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.children = []
    def addChild(self, child):
        self.children.append(child)