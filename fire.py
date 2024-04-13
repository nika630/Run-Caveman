import pygame


import settings as setting
from sounds import fire_sound


class Fire(pygame.sprite.Sprite):  # оборона игрока
    def __init__(self, pos, *group):
        super().__init__(*group)
        self.fire_img = [pygame.image.load(name).convert_alpha() for name in setting.FIRE]

        self.image = self.fire_img[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] + 40
        self.rect.y = pos[1] + 40
        self.speed = 6
        self.count = 0

    def counter(self):
        if self.count >= 8:
            if self.count == 0:
                pygame.mixer.Sound.play(fire_sound)
            self.count = 0
        else:
            self.count += 1

    def get_position(self, stone):
        return self.rect.x

    def update(self, all_enemy):
        self.image = self.fire_img[self.count // 3]
        self.rect.x += self.speed
        self.counter()
