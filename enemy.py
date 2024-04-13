from random import randrange, choice

import pygame

import settings as setting
from sounds import kill_dino, collision
from game_over import game_over


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.enemy_motion = [pygame.image.load(name).convert_alpha() for name in setting.ENEMY]
        self.falling_enemy = pygame.image.load(r'images/enemy/5.png').convert_alpha()
        self.image = self.enemy_motion[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = setting.WINDOW_WIDTH
        self.rect.y = randrange(100, 300)

        self.width = 69
        self.height = 85
        self.count = 0
        self.track = choice([-1, 1])  # направление полёта
        self.killed = False
        self.first_collide = True

    def counter(self):
        if self.count >= 29:
            self.count = 0
        else:
            self.count += 1

    def update(self, player, all_fire, score):
        for fire in all_fire:
            if pygame.sprite.collide_mask(self, fire):  # столкновение с огнем
                pygame.mixer.Sound.play(kill_dino)
                self.killed = True
        if self.killed:  # падение после столкновения
            self.image = self.falling_enemy
            self.rect.y += setting.SPEED
        else:
            if self.first_collide and pygame.sprite.collide_mask(self, player):  # столкновение с игроком
                pygame.mixer.Sound.play(collision)
                self.first_collide = False
                result = setting.sql.execute('''SELECT count FROM Hearts ''').fetchall()[0][0]
                if result == 1:
                    setting.sql.execute('''UPDATE Hearts SET count = ? ''', (result - 1,))
                    game_over(score)
                else:
                    result -= 1
                    setting.sql.execute('''UPDATE Hearts SET count = ? ''', (result,))
                    setting.db.commit()
            else:
                img = self.enemy_motion[self.count // 7]
                self.image = img
                if player.rect.x - 20 <= self.rect.x <= player.rect.x + 50:
                    self.rect.y += setting.SPEED

                else:
                    self.rect.x -= setting.SPEED
                    self.rect.y += setting.SPEED * self.track
                    if self.rect.y > (setting.WINDOW_HEIGHT - setting.LAND - self.height - 10) or self.rect.y < 0:
                        self.track *= -1
                self.counter()

        if not self.first_collide:
            self.kill()
