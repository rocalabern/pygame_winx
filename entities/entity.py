import pygame
from pygame import *


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.collides = False
        self.has_grip = False
        self.item = False
        self.collectable = False
        self.transformed = False
        self.fly = False

