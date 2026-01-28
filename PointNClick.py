#import standard libraries
import os

#import 3rd party libraries
import pygame

#import custom libraries
import levelHandeling

#initalise libraries
pygame.init()

#create window stuff
windowWidth = 600
windowHeight = 600
window = pygame.display.set_mode((windowWidth, windowHeight))

#load images
bg = pygame.image.load(os.path.join("images", "bg", "bg.png"))
wallTexture = pygame.image.load(os.path.join("images", "bg", "wall_texture.png"))
barrierTexture = pygame.image.load(os.path.join("images", "bg", "border_texture.png"))
barriers = {}
walls = {}

#other setup
grabbed = True
pygame.event.set_grab(grabbed) #want cursor to be locked into the window
frame = 0
frameCounter = 0

#useful classes
class MouseControl():
    def __init__(self):
        self.currentPos = pygame.mouse.get_pos()
        self.lastPos = self.currentPos
    def checkCollision(self):
        self.currentPos = pygame.mouse.get_pos()
        #check barrier first
        for barrier in barriers.values():
            if barrier.clipline((self.currentPos[0], self.currentPos[1]), (self.lastPos[0], self.lastPos[1])):
                print("hit")
        for wall in walls.values():
            if wall.clipline((self.currentPos[0], self.currentPos[1]), (self.lastPos[0], self.lastPos[1])):
                pygame.mouse.set_pos(self.lastPos[0], self.lastPos[1])
        self.lastPos = pygame.mouse.get_pos()

#TEMPORARY
#load file
def loadLevel(path):
    layout = levelHandeling.loadLevelLayout(path)
    for wall in layout["wall"]:
        walls[wall] = pygame.Rect(layout["wall"][wall]["x"], layout["wall"][wall]["y"], layout["wall"][wall]["width"], layout["wall"][wall]["height"])
    for barrier in layout["barrier"]:
        barriers[barrier] = pygame.Rect(layout["barrier"][barrier]["x"], layout["barrier"][barrier]["y"], layout["barrier"][barrier]["width"], layout["barrier"][barrier]["height"])
    elements = {
        "walls": walls,
        "barriers": barriers,
    }
    return elements
layout = loadLevel("layout.xml")


def drawElements():
    for wall in layout["walls"].values():
        window.blit(wallTexture, wall, wall)
    for barrier in layout["barriers"].values():
        window.blit(barrierTexture, barrier, (barrier.x, barrier.y + 600 * frame, barrier.width, barrier.height))

#classes definitons
mouse = MouseControl()


#main game loop
run = True
while run:
    #wipe screen
    window.blit(bg, (0, 0))
    drawElements()
    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #this will pause later
                grabbed = not grabbed
                pygame.event.set_grab(grabbed) 
    if frameCounter >= 50:
        frame += 1
        frameCounter = 0
    else:
        #TODO: Add frame rate independence?
        frameCounter += 1
    if frame > 15:
        frame = 0
    mouse.checkCollision()
    #update window
    pygame.display.update()

#close pygame
pygame.quit()