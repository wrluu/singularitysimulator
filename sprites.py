import pygame
import os
from settings import *


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, obj_type, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(os.path.join('', 'images', f'{obj_type}.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.obj_type = obj_type
        self.interacted = False
