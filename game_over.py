import pygame

import settings as setting
from create import print_text


def game_over(score):
    # фиксируем текущий счет и уровень
    setting.sql.execute('''INSERT INTO User (score, level) VALUES (?,?)''', (score, setting.LEVEL))
    max_score = setting.sql.execute('''SELECT MAX(score) FROM User''').fetchall()[0][0]
    setting.db.commit()

    pygame.mixer.music.stop()
    clock = pygame.time.Clock()

    action_text = print_text(f'Game Over', 70)
    max_score_text = print_text(f'YOUR SCORE: {score} | MAX SCORE: {max_score}', 30)
    exit_text = print_text(f'Press SPACE to start again', 25)
    action_rect = action_text.get_rect(center=(setting.WINDOW_WIDTH // 2, setting.WINDOW_HEIGHT // 2 - 70))
    max_score_rect = max_score_text.get_rect(center=(setting.WINDOW_WIDTH // 2, setting.WINDOW_HEIGHT // 2))
    exit_rect = exit_text.get_rect(center=(setting.WINDOW_WIDTH // 2, setting.WINDOW_HEIGHT // 2 + 50))

    setting.sql.execute("""INSERT INTO Hearts VALUES(?) """, (3,))
    setting.db.commit()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            running = False
            setting.NEW_GAME = True
            setting.new_game()

        pygame.draw.rect(setting.screen, 'Purple', exit_rect)
        pygame.draw.rect(setting.screen, 'Purple', exit_rect, 10)
        setting.screen.blit(action_text, action_rect)
        pygame.draw.rect(setting.screen, 'Yellow', max_score_rect)
        pygame.draw.rect(setting.screen, 'Yellow', max_score_rect, 10)
        setting.screen.blit(max_score_text, max_score_rect)
        setting.screen.blit(exit_text, exit_rect)

        pygame.display.update()
        clock.tick(setting.FPS)
