import pygame

import settings as setting
from create import print_text
from menu import Button
from sounds import win_sound, btn_sound
from termit import terminate


def end_of_game(score):
    max_score = setting.sql.execute('''SELECT MAX(score) FROM User''').fetchall()[0][0]

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(win_sound)
    clock = pygame.time.Clock()

    # счёт игрока
    max_score_text = print_text(f'YOUR SCORE: {score} | MAX SCORE: {max_score}', 30)
    max_score_rect = max_score_text.get_rect(center=(setting.WINDOW_WIDTH // 2,
                                                     setting.WINDOW_HEIGHT - setting.LAND - 100))
    winner_img = pygame.image.load(r'images/other/you_win.png').convert_alpha()
    winner_rect = winner_img.get_rect(center=(setting.WINDOW_WIDTH // 2, setting.WINDOW_HEIGHT // 2))

    # переиграть или выйти из игры
    play_btn = Button((200, setting.WINDOW_HEIGHT // 2),
                      setting.MENU_IMG[0], setting.MENU_IMG[1])
    exit_btn = Button((700, setting.WINDOW_HEIGHT // 2),
                      setting.MENU_IMG[4], setting.MENU_IMG[5])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        mouse = pygame.mouse.get_pos()

        if play_btn.rect.collidepoint(mouse):
            play_btn.image = play_btn.img2
            click = pygame.mouse.get_pressed()
            if click[0]:
                pygame.mixer.Sound.play(btn_sound)
                pygame.time.delay(300)
                setting.NEW_GAME = True
                running = False
        else:
            play_btn.image = play_btn.img1

        if exit_btn.rect.collidepoint(mouse):
            exit_btn.image = exit_btn.img2
            click = pygame.mouse.get_pressed()
            if click[0]:
                pygame.mixer.Sound.play(btn_sound)
                pygame.time.delay(300)
                terminate()
        else:
            exit_btn.image = exit_btn.img1

        setting.screen.blit(winner_img, winner_rect)
        pygame.draw.rect(setting.screen, 'Yellow', max_score_rect)
        pygame.draw.rect(setting.screen, 'Yellow', max_score_rect, 10)
        setting.screen.blit(max_score_text, max_score_rect)
        setting.screen.blit(play_btn.image, play_btn.rect)
        setting.screen.blit(exit_btn.image, exit_btn.rect)

        pygame.display.update()
        clock.tick(setting.FPS)
