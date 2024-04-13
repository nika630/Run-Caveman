import pygame

import settings as settings
from create import print_text


def create_btn(img_name, pos):  # генератор кнопок
    img = pygame.image.load(img_name)
    img_rect = img.get_rect(topright=pos)
    return img, img_rect


class Game:  # логика игры
    def __init__(self, player, stone, screen):
        self.screen = screen
        self.up = pygame.image.load(settings.BG_UP).convert_alpha()
        self.down = pygame.image.load(settings.BG_DOWN).convert_alpha()
        self.player = player
        self.stone = stone
        self.bg_up_x = 0
        self.bg_down_x = 0
        self.level = 1
        self.font_type = pygame.font.Font(r'font/PingPong.ttf', 50)
        self.score = 0

    def background_motion(self, screen):  # отрисовка фона переднего и заднего плана
        screen.blit(self.up, (self.bg_up_x, 0))
        screen.blit(self.up, (self.bg_up_x + settings.WINDOW_WIDTH, 0))
        screen.blit(self.down, (self.bg_down_x, 0))
        screen.blit(self.down, (self.bg_down_x + settings.WINDOW_WIDTH, 0))

        if self.bg_down_x <= -settings.WINDOW_WIDTH:
            self.bg_down_x = 0
        else:
            self.bg_down_x -= settings.SPEED

        if self.bg_up_x <= -settings.WINDOW_WIDTH:
            self.bg_up_x = 0
        else:
            self.bg_up_x -= settings.SPEED / 2

    def out_of_window(self, all_stones, all_enemy, all_fire, all_hearts):  # подсчет очков и удаление спрайтов
        for stone in all_stones:
            if stone.rect.x < -100:
                stone.kill()
                self.score += 10

        for enemy in all_enemy:
            if enemy.rect.y > settings.WINDOW_HEIGHT + 100:
                enemy.kill()
                self.score += 50
            elif enemy.rect.x < -100:
                enemy.kill()

        for fire in all_fire:
            if fire.rect.x > settings.WINDOW_WIDTH + 100:
                fire.kill()

        for heart in all_hearts:
            if heart.rect.x > settings.WINDOW_WIDTH + 100:
                heart.kill()

        return self.score

    def change_timer(self, timer, seconds):  # изменение таймера игры
        seconds += 1000
        pygame.time.set_timer(timer, seconds)

    def lvl(self, lvl):  # отображение текущего уровня в левом верхнем углу
        lvl_text = print_text(f'LEVEL: {lvl}', 20)
        lvl_rect = lvl_text.get_rect(topleft=(20, 90))
        self.screen.blit(lvl_text, lvl_rect)

    def show_lvl(self, lvl):  # отображение уровня в центре экрана
        lvl_text = print_text(f'LEVEL {lvl}', 50)
        lvl_rect = lvl_text.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2))
        self.screen.blit(lvl_text, lvl_rect)

    def game_score(self, score):  # отображение изменения счета игры
        score_surf = print_text(f'Score: {score}', 20)
        score_rect = score_surf.get_rect(topleft=(20, 60))
        self.screen.blit(score_surf, score_rect)


