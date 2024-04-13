import pygame

import settings as setting
from create import print_text


def pause():
    clock = pygame.time.Clock()
    action_text = print_text('Paused', 70)
    action_rect = action_text.get_rect(center=(setting.WINDOW_WIDTH // 2, setting.WINDOW_HEIGHT // 2 - 70))
    exit_text = print_text('Press SPACE to continue', 20)
    exit_rect = exit_text.get_rect(center=(setting.WINDOW_WIDTH // 2, setting.WINDOW_HEIGHT // 2 + 50))
    pygame.mixer.music.pause()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.draw.rect(setting.screen, 'Yellow', exit_rect)
        pygame.draw.rect(setting.screen, 'Yellow', exit_rect, 10)
        setting.screen.blit(action_text, action_rect)
        setting.screen.blit(exit_text, exit_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            paused = False

        pygame.display.update()
        clock.tick(setting.FPS)
    pygame.mixer.music.unpause()
