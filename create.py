import os

import pygame


def print_text(text, font_size=20, font_color=(0, 0, 0)):
    font_type = pygame.font.Font('font/PingPong.ttf', font_size)
    text = font_type.render(text, True, font_color)
    return text


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
