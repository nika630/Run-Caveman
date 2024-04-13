import pygame

import settings as setting


class Player(pygame.sprite.Sprite):
    width = 80
    height = 80

    def __init__(self, *group):
        super().__init__(*group)
        # направление движения игрока
        self.go_right = [pygame.image.load(name).convert_alpha() for name in setting.GO_RIGHT]
        self.go_left = [pygame.image.load(name).convert_alpha() for name in setting.GO_LEFT]
        self.jump_right = pygame.image.load(r'images/jump/jump_right.png').convert_alpha()
        self.jump_left = pygame.image.load(r'images/jump/jump_left.png').convert_alpha()

        self.image = self.jump_right
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 50
        self.rect.y = setting.WINDOW_HEIGHT - Player.height - setting.LAND + 10

        self.count = 0
        self.sprite_shift = 5
        self.jump_height = 27
        self.jump_count = 0
        self.left = False

    def get_position(self):
        return self.rect.x, self.rect.y

    def set_position(self, position):
        self.rect.x, self.rect.y = position

    def jump(self):
        self.image = self.jump_right
        if self.jump_height > -26:
            self.jump_count += 1
            self.rect.y -= self.jump_height // 2.5
            self.jump_height -= 1
        else:
            self.jump_height = 27
            self.jump_count = 0

    def go_right(self):
        self.rect.x += (setting.SPEED + 1)
        if self.jump_count == 0:
            self.image = self.go_right[self.count // self.sprite_shift]
        else:
            self.image = self.jump_right

    def go_left(self, left):
        self.left = left
        if self.jump_count == 0:
            self.image = self.go_left[self.count // self.sprite_shift]
        else:
            self.image = self.jump_left
        self.rect.x -= (setting.SPEED + 1)

    def counter(self):
        if self.count >= 39:
            self.count = 0
        else:
            self.count += 1

    def update(self, make_jump=False):
        if make_jump or self.jump_count != 0:
            self.jump()
        elif self.left and self.jump_count == 0:
            self.image = self.go_left[self.count // self.sprite_shift]
        else:
            self.image = self.go_right[self.count // self.sprite_shift]
        self.counter()
        self.left = False
