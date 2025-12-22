#import standard libraries

#import 3rd party libraries
import pygame

#initalise libraries
pygame.init()

#create window stuff
windowWidth = 600
windowHeight = 600

window = pygame.display.set_mode((windowWidth, windowHeight))

#main game loop
run = True
while run:
    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#close pygame
pygame.quit()