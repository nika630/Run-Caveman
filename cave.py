import pygame

import settings as setting
from end_of_game import end_of_game


class Cave(pygame.sprite.Sprite):  # пещера
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.image.load(r'images/other/cave.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = setting.WINDOW_WIDTH
        self.rect.y = setting.WINDOW_HEIGHT - setting.LAND - 110
        self.first_collide = True

    def set_position(self):
        self.rect.x = setting.WINDOW_WIDTH

    def update(self, player, score):
        self.rect.x -= setting.SPEED
        if pygame.sprite.collide_mask(self, player) and self.first_collide:
            end_of_game(score)
            self.first_collide = False
            print('lvl_up')

        if self.rect.x < - 100:
            print('kill stone')
            self.kill()
