# фоновая музыка
import pygame

pygame.init()

pygame.mixer.music.load(r'sounds/back_sound.mp3')
pygame.mixer.music.set_volume(0.1)

collision = pygame.mixer.Sound(r'sounds/collision.mp3')  # столкновение
heart_sound = pygame.mixer.Sound(r'sounds/heart+.mp3')  # подобрал жизнь
kill_dino = pygame.mixer.Sound(r'sounds/heat.mp3')  # убил врага
fire_sound = pygame.mixer.Sound(r'sounds/fire.mp3')  # выстрел огнем
btn_sound = pygame.mixer.Sound(r'sounds/button.wav')  # нажатие на кнопки в игре
win_sound = pygame.mixer.Sound(r'sounds/win.mp3')  # победа
