import pygame


import settings as setting


class Heart(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.image.load(r'images/other/heart.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.heart_width = 30
        self.rect.x = setting.WINDOW_WIDTH
        self.rect.y = setting.WINDOW_HEIGHT - setting.LAND - 150

    def update(self, player):
        if pygame.sprite.collide_mask(self, player):
            heart_count = setting.sql.execute('''SELECT count FROM Hearts''').fetchall()[0][0]
            if heart_count < 5:  # расширение количества жизней до 5
                heart_count += 1
                setting.sql.execute('''UPDATE Hearts SET count = ? ''', (heart_count,))
            self.kill()
        self.rect.x -= setting.SPEED


def heart_balance(heart_width=30):  # текущее количество жизней
    heart_count = setting.sql.execute('''SELECT count FROM Hearts''').fetchall()[0][0]
    image = pygame.image.load(r'images/other/heart.png').convert_alpha()
    pos = 20
    for i in range(heart_count):
        setting.screen.blit(image, (pos, 20))
        pos += heart_width + 5
