import pygame
import os
from settings import *
from player import Player
from sprites import CollisionSprite
from npc import NPC
from static_npc import Ksu, Yarik
from pytmx.util_pygame import load_pygame

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH // 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT // 2

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Singularity Simulator")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dialog_active = False
        self.dialog_index = 0
        self.current_dialog = []
        self.start_screen_active = True
        self.game_time = 530
        self.interaction_cooldown = 0
        self.npc_interacted = {'ksu': False, 'yarik': False}
        self.computer_interaction_complete = False

        self.all_sprites = Camera()
        self.collision_sprites = pygame.sprite.Group()

        self.player = Player((2700, 500), self.all_sprites, collision_sprites=self.collision_sprites)

        self.npc = NPC((1200, 600), [self.all_sprites, self.collision_sprites])
        self.ksu = Ksu((1480, 500), [self.all_sprites, self.collision_sprites])
        self.yarik = Yarik((2420, 370), [self.all_sprites, self.collision_sprites])

        self.dialog_images = {
            'npc': [pygame.image.load(os.path.join('', 'images', f'npc_{i}.png')).convert_alpha() for i in range(1, 7)],
            'ksu': [pygame.image.load(os.path.join('', 'images', f'ksu_{i}.png')).convert_alpha() for i in range(1, 5)],
            'yarik': [pygame.image.load(os.path.join('', 'images', f'yarik_{i}.png')).convert_alpha() for i in range(1, 4)],
            'computer_1': [pygame.image.load(os.path.join('', 'images', 'computer_1.png')).convert_alpha()],
            'list_1': [pygame.image.load(os.path.join('', 'images', 'list_1.png')).convert_alpha()],
            'list_2': [pygame.image.load(os.path.join('', 'images', 'list_2.png')).convert_alpha()],
            'list_3': [pygame.image.load(os.path.join('', 'images', 'list_3.png')).convert_alpha()],
            'finish': [pygame.image.load(os.path.join('', 'images', 'finish.png')).convert_alpha()],
            'smoke': [pygame.image.load(os.path.join('', 'images', f'smoke_{i}.png')).convert_alpha() for i in range(1, 3)],
            'fridge': [pygame.image.load(os.path.join('', 'images', f'fridge_{i}.png')).convert_alpha() for i in range(1, 3)],
            'table': [pygame.image.load(os.path.join('', 'images', f'table_{i}.png')).convert_alpha() for i in range(1, 3)]
        }

        self.start_image = pygame.image.load(os.path.join('', 'images', 'start.png')).convert_alpha()

        self.setup()

    def setup(self):
        map = load_pygame(os.path.join('', 'map1.tmx'))
        layers_to_load = ['Слой объектов 1', 'Слой объектов 2']
        for layer_name in layers_to_load:
            for obj in map.get_layer_by_name(layer_name):
                obj_type = obj.type
                if obj_type:
                    if obj_type in ['computer_1', 'computer_2']:
                        x = (WINDOW_WIDTH - self.start_image.get_width()) // 2
                        y = (WINDOW_HEIGHT - self.start_image.get_height()) // 2
                        CollisionSprite((x, y), obj_type, (self.collision_sprites, self.all_sprites))
                    else:
                        CollisionSprite((obj.x, obj.y), obj_type, (self.collision_sprites, self.all_sprites))

    def run(self):
        try:
            while self.running:
                dt = self.clock.tick() / 1000
                self.game_time += dt * 30

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.start_screen_active:
                            self.start_screen_active = False
                        elif not self.dialog_active:
                            self.check_interaction()
                        else:
                            self.next_dialog()

                if not self.start_screen_active and not self.dialog_active:
                    self.all_sprites.update(dt)

                self.display_surface.fill('#696969')

                if self.start_screen_active:
                    self.display_surface.blit(self.start_image, (0, 0))
                else:
                    self.all_sprites.custom_draw(self.player)

                    if self.dialog_active:
                        self.display_surface.fill('black')
                        image = self.current_dialog[self.dialog_index]
                        rect = image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                        self.display_surface.blit(image, rect.topleft)

                self.draw_timer()
                pygame.display.update()
        except KeyboardInterrupt:
            self.running = False

        pygame.quit()

    def check_interaction(self):
        if self.interaction_cooldown > 0:
            return

        mouse_pos = pygame.mouse.get_pos()
        adjusted_mouse_pos = mouse_pos[0] + self.all_sprites.offset.x, mouse_pos[1] + self.all_sprites.offset.y
        mouse_rect = pygame.Rect(adjusted_mouse_pos, (1, 1))

        priority_objects = ['computer', 'smoke', 'fridge', 'table']

        clicked_sprite = None
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(mouse_rect):
                if hasattr(sprite, 'obj_type') and sprite.obj_type in priority_objects:
                    clicked_sprite = sprite
                    break
                elif clicked_sprite is None:
                    clicked_sprite = sprite

        if clicked_sprite:
            if isinstance(clicked_sprite, NPC):
                self.start_dialog('npc')
            elif isinstance(clicked_sprite, Ksu):
                self.start_dialog('ksu')
                self.npc_interacted['ksu'] = True
            elif isinstance(clicked_sprite, Yarik):
                self.start_dialog('yarik')
                self.npc_interacted['yarik'] = True
            elif hasattr(clicked_sprite, 'obj_type'):
                if clicked_sprite.obj_type == 'computer':
                    self.start_dialog('computer_1')
                elif clicked_sprite.obj_type == 'smoke':
                    self.start_dialog('smoke')
                elif clicked_sprite.obj_type == 'fridge':
                    self.start_dialog('fridge')
                elif clicked_sprite.obj_type == 'table':
                    self.start_dialog('table')
            self.interaction_cooldown = 1

    def start_dialog(self, character):
        self.dialog_active = True
        self.dialog_index = 0
        if character == 'computer_1':
            self.current_dialog = self.dialog_images['computer_1'] + self.dialog_images['list_1'] + self.dialog_images['list_2'] + self.dialog_images['list_3'] + self.dialog_images['finish']
        else:
            self.current_dialog = self.dialog_images[character]

    def next_dialog(self):
        self.dialog_index += 1
        if self.dialog_index >= len(self.current_dialog):
            self.dialog_active = False
            self.interaction_cooldown = 0
            if self.current_dialog == self.dialog_images['computer_1'] + self.dialog_images['list_1'] + self.dialog_images['list_2'] + self.dialog_images['list_3'] + self.dialog_images['finish']:
                self.computer_interaction_complete = True
                self.running = False

    def draw_timer(self):
        minutes = int(self.game_time // 60) % 60
        hours = int(self.game_time // 3600) % 24 + 8
        time_string = f"{hours:02}:{minutes:02}"
        font = pygame.font.Font(None, 36)
        text_surface = font.render(time_string, True, 'white')
        self.display_surface.blit(text_surface, (10, WINDOW_HEIGHT - 30))

if __name__ == "__main__":
    game = Game()
    game.run()

