import pygame
import os
from settings import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.sprites = {
            'up': pygame.image.load(os.path.join('..', 'images', 'npc_down.png')).convert_alpha(),
            'down': pygame.image.load(os.path.join('..', 'images', 'npc_up.png')).convert_alpha()
        }
        self.image = self.sprites['down']
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(self.rect.center)
        self.direction = pygame.Vector2(0, 1)
        self.speed = 70
        self.y_min = 400
        self.y_max = 900

    def update(self, dt):
        # Обновляем позицию
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = round(self.pos.y)

        # Проверяем достижение границ и меняем направление
        if self.rect.top <= self.y_min or self.rect.bottom >= self.y_max:
            self.direction.y = -self.direction.y
            self.image = self.sprites['up'] if self.direction.y < 0 else self.sprites['down']

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
