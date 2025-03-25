import pygame
import os
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups, collision_sprites):
        super().__init__(*groups)
        self.sprites = {
            'up': pygame.image.load(os.path.join('', 'images', 'player_up.png')).convert_alpha(),
            'down': pygame.image.load(os.path.join('', 'images', 'player_down.png')).convert_alpha(),
            'left': pygame.image.load(os.path.join('', 'images', 'player_left.png')).convert_alpha(),
            'right': pygame.image.load(os.path.join('', 'images', 'player_right.png')).convert_alpha()
        }
        self.image = self.sprites['down']
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(self.rect.center)

        self.direction = pygame.Vector2()
        self.speed = 400
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.pos.x += self.direction.x * self.speed * dt
            self.rect.centerx = round(self.pos.x)
            self.check_collision('horizontal')

            self.pos.y += self.direction.y * self.speed * dt
            self.rect.centery = round(self.pos.y)
            self.check_collision('vertical')

    def check_collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                    self.pos.x = self.rect.centerx
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    self.pos.y = self.rect.centery

    def update(self, dt):
        self.input()
        self.move(dt)
        self.update_sprite()

    def update_sprite(self):
        if self.direction.y > 0:
            self.image = self.sprites['down']
        elif self.direction.y < 0:
            self.image = self.sprites['up']
        elif self.direction.x > 0:
            self.image = self.sprites['right']
        elif self.direction.x < 0:
            self.image = self.sprites['left']
