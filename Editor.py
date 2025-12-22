#import standard libraries

#import 3rd party libraries
import pygame

#initalise libraries
pygame.init()

#define window stuff
windowWidth = 600
windowHeight = 600

window = pygame.display.set_mode((windowWidth, windowHeight))

#main loop
run = True
while run:
    #event handeler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#close pygame stuff
pygame.quit()