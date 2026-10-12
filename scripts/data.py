'''asset loading and storage'''

import os

import pygame

images = {}

def loadImages():
    global images
    images["wall"] = pygame.image.load(os.path.join("assets", "images", "bg", "wall_texture.png")),
    images["barrier"] = pygame.image.load(os.path.join("assets", "images", "bg", "border_texture.png")),

def getImage(name):
    try:
        return images[name]
    except():
        return pygame.Surface((0, 0))