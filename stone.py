from random import randrange

import pygame

import settings as setting
from game_over import game_over
from sounds import collision


class Stone(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.x = None
        self.stone_img = [pygame.image.load(name).convert_alpha() for name in setting.STONE_IMG]
        self.n = randrange(0, len(setting.STONE_IMG))
        self.image = self.stone_img[self.n]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = setting.WINDOW_WIDTH
        self.rect.y = setting.WINDOW_HEIGHT - setting.LAND - setting.STONE_HEIGHT[self.n]
        self.first_collide = True

    def get_position(self, stone):
        self.x = stone.rect.x
        return self.x

    def set_position(self, stone, pos):
        stone.rect.x = pos
        self.x = stone.rect.x

    def stone_score(self):
        pass

    def update(self, player, score):
        if self.first_collide:
            if pygame.sprite.collide_mask(self, player):
                pygame.mixer.Sound.play(collision)
                self.first_collide = False
                result = setting.sql.execute('''SELECT count FROM Hearts''').fetchall()[0][0]
                if result == 1:
                    game_over(score)
                else:
                    result -= 1
                    setting.sql.execute('''UPDATE Hearts SET count = ?''', (result,))
                    setting.db.commit()

            self.rect.x -= setting.SPEED
        else:
            self.kill()
