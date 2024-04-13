import pygame

from sounds import btn_sound
from create import print_text
import settings as setting
from termit import terminate


class Button:  # генератор кнопок
    def __init__(self, pos, img1, img2):
        self.img1 = pygame.image.load(img1).convert_alpha()
        self.img2 = pygame.image.load(img2).convert_alpha()
        self.image = self.img1
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)


def menu(fist_btn=False):
    clock = pygame.time.Clock()
    pygame.display.set_caption('Menu')

    background = pygame.image.load(r'Backgrounds/background2.png').convert_alpha()  # фон
    menu_text = print_text('MENU', 100)
    menu_rect = menu_text.get_rect(center=(setting.WINDOW_WIDTH // 2, 100))

    # отображение кнопки "play" или "continue" в зависимости от времени вызова меню
    if fist_btn:
        play_btn = Button((setting.WINDOW_WIDTH // 2, setting.WINDOW_HEIGHT // 2 - 60),
                          setting.MENU_IMG[6], setting.MENU_IMG[7])
    else:
        play_btn = Button((setting.WINDOW_WIDTH // 2, setting.WINDOW_HEIGHT // 2 - 60),
                          setting.MENU_IMG[0], setting.MENU_IMG[1])
    # управление игрой
    option_btn = Button((setting.WINDOW_WIDTH // 2, setting.WINDOW_HEIGHT // 2 + 30),
                        setting.MENU_IMG[2], setting.MENU_IMG[3])
    # выход
    exit_btn = Button((setting.WINDOW_WIDTH // 2, setting.WINDOW_HEIGHT // 2 + 110),
                      setting.MENU_IMG[4], setting.MENU_IMG[5])
    run_menu = True
    while run_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run_menu = False

        setting.screen.blit(background, (0, 0))
        setting.screen.blit(menu_text, menu_rect)

        mouse = pygame.mouse.get_pos()

        if play_btn.rect.collidepoint(mouse):
            play_btn.image = play_btn.img2
            click = pygame.mouse.get_pressed()
            if click[0]:
                pygame.mixer.Sound.play(btn_sound)
                pygame.time.delay(300)
                if fist_btn:
                    run_menu = False
                else:
                    setting.NEW_GAME = True
                    run_menu = False
        else:
            play_btn.image = play_btn.img1

        if option_btn.rect.collidepoint(mouse):
            option_btn.image = option_btn.img2
            click = pygame.mouse.get_pressed()
            if click[0]:
                pygame.mixer.Sound.play(btn_sound)
                pygame.time.delay(300)
                options()
        else:
            option_btn.image = option_btn.img1

        if exit_btn.rect.collidepoint(mouse):
            exit_btn.image = exit_btn.img2
            click = pygame.mouse.get_pressed()
            if click[0]:
                pygame.mixer.Sound.play(btn_sound)
                pygame.time.delay(300)
                terminate()
        else:
            exit_btn.image = exit_btn.img1

        setting.screen.blit(play_btn.image, play_btn.rect)
        setting.screen.blit(option_btn.image, option_btn.rect)
        setting.screen.blit(exit_btn.image, exit_btn.rect)

        pygame.display.update()
        clock.tick(setting.FPS)


def options():
    clock = pygame.time.Clock()
    pygame.display.set_caption('Menu')

    background = pygame.image.load(r'images/menu/options.jpg').convert_alpha()

    back_btn = Button((40, 40), r'images/menu/back_btn.png', r'images/menu/back_btn_2.png')

    run_menu = True
    while run_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run_menu = False

        mouse = pygame.mouse.get_pos()

        if back_btn.rect.collidepoint(mouse):
            back_btn.image = back_btn.img2
            click = pygame.mouse.get_pressed()
            if click[0]:
                pygame.mixer.Sound.play(btn_sound)
                pygame.time.delay(300)
                run_menu = False
        else:
            back_btn.image = back_btn.img1

        setting.screen.blit(background, (0, 0))
        setting.screen.blit(back_btn.image, back_btn.rect)

        pygame.display.update()
        clock.tick(setting.FPS)
