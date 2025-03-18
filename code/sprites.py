from settings import *

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups, collision_sprites):
        super().__init__(*groups)
        self.image = pygame.Surface(size)
        self.image.fill('white')
        self.rect = self.image.get_rect(center=pos)