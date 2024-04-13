from sys import exit

import random

from cave import Cave
from enemy import Enemy
from fire import Fire
from heart import heart_balance, Heart
from menu import menu
from pause import pause
from player import Player
from game import *
from sounds import btn_sound
from stone import Stone
import settings as setting

pygame.init()


def main():
    menu()  # вызов стартового окна меню
    setting.new_db()

    pygame.display.set_caption('Run Caveman!')
    pygame.mixer.music.play(-1)

    make_jump = False  # нужно ли делать прыжок

    # таймер появление врагов в игре (изменяется по мере усложнения уровня)
    clock = pygame.time.Clock()
    timer = pygame.USEREVENT + 1
    seconds = 5000
    pygame.time.set_timer(timer, seconds)

    # переменные для отслеживания состояний в игре
    lvl_time = pygame.time.get_ticks()
    score = 0
    lvl_score = 0
    heart_score = 0

    player_sprite = pygame.sprite.Group()  # игрок
    all_enemy = pygame.sprite.Group()  # враги
    all_stones = pygame.sprite.Group()  # препятствия (камни)
    all_fire = pygame.sprite.Group()  # стрельба огнем
    all_hearts = pygame.sprite.Group()  # дополнительные жизни
    all_caves = pygame.sprite.Group()  # пещера

    player = Player(player_sprite)
    stone = Stone(all_stones)  # первый камень на экране
    game = Game(player, stone, setting.screen)
    cave = Cave(all_caves)

    # кнопки управления в правой верхней части экрана
    again_btn, again_rect = create_btn(r'images/menu/again_btn.png', (setting.WINDOW_WIDTH - 200, 15))
    pause_btn, pause_rect = create_btn(r'images/menu/pause_btn.png', (setting.WINDOW_WIDTH - 140, 15))
    menu_btn, menu_rect = create_btn(r'images/menu/menu_btn.png', (setting.WINDOW_WIDTH - 80, 15))
    exit_btn, exit_rect = create_btn(r'images/menu/exit_btn.png', (setting.WINDOW_WIDTH - 20, 15))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # пауза по нажатию клавиши
                    pause()
                if event.key == pygame.K_SPACE or event.key == pygame.K_r:  # стрельба по врагам
                    Fire(Player.get_position(player), all_fire)
                if event.key == pygame.K_w or event.key == pygame.K_UP:  # прыжок
                    make_jump = True
            if event.type == timer:  # появление врагов в игре
                Enemy(all_enemy)
                game.change_timer(timer, seconds)

        current_time = pygame.time.get_ticks()  # текущее время в игре
        keys = pygame.key.get_pressed()

        # направление движения игрока
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if player.rect.x > 0:
                Player.go_left(player, True)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if player.rect.x < 870:
                Player.go_right(player)

        all_enemy.update(player, all_fire, score)
        all_stones.update(player, score)
        player_sprite.update(make_jump)
        all_fire.update(all_enemy)
        all_hearts.update(player)

        make_jump = False

        stone_x = stone.get_position(stone)  # логика появлений препятствий
        if setting.WINDOW_WIDTH - stone_x >= 150:
            pos = random.randrange(0, 600)
            pos += setting.WINDOW_WIDTH
            stone = Stone(all_stones)
            stone.set_position(stone, pos)

        game.background_motion(setting.screen)
        all_hearts.draw(setting.screen)
        all_caves.draw(setting.screen)
        player_sprite.draw(setting.screen)
        all_stones.draw(setting.screen)
        all_fire.draw(setting.screen)
        all_enemy.draw(setting.screen)
        heart_balance()  # отображение жизни игрока

        # работа кнопок управления игрой
        setting.screen.blit(menu_btn, menu_rect)
        setting.screen.blit(exit_btn, exit_rect)
        setting.screen.blit(pause_btn, pause_rect)
        setting.screen.blit(again_btn, again_rect)

        mouse = pygame.mouse.get_pos()
        if menu_rect.collidepoint(mouse):
            click = pygame.mouse.get_pressed()
            if click[0]:
                pygame.mixer.Sound.play(btn_sound)
                menu(fist_btn=True)
        if exit_rect.collidepoint(mouse):
            click = pygame.mouse.get_pressed()
            if click[0]:
                pygame.mixer.Sound.play(btn_sound)
                pygame.quit()
                exit()
        if pause_rect.collidepoint(mouse):
            click = pygame.mouse.get_pressed()
            if click[0]:
                pygame.mixer.Sound.play(btn_sound)
                pause()
        if again_rect.collidepoint(mouse):
            click = pygame.mouse.get_pressed()
            if click[0]:
                pygame.mixer.Sound.play(btn_sound)
                pygame.time.delay(300)
                setting.NEW_GAME = True

        # оповещение о смене уровня
        if score - lvl_score > 300:
            setting.lvl_up()
            lvl_score = score
            print(lvl_score, setting.SPEED)
            lvl_time = current_time

        if current_time - lvl_time < 3000:  # оповещение игрока о смене уровня
            game.show_lvl(setting.LEVEL)

        # появление дополнительных жизней
        if score - heart_score > 500:
            heart_score = score
            Heart(all_hearts)

        # окончание игры, последний уровень
        if setting.LEVEL == 10:
            cave.update(player, score)

        # удаление спрайтов за пределами окна и подсчет очков игры
        score = game.out_of_window(all_stones, all_enemy, all_fire, all_hearts)
        game.game_score(score)
        game.lvl(setting.LEVEL)

        if setting.NEW_GAME:
            setting.sql.execute('''UPDATE Hearts SET count = ? ''', (3,))  # обновление жизней
            pygame.mixer.music.play(-1)
            timer = pygame.USEREVENT + 1
            seconds = 5000
            pygame.time.set_timer(timer, seconds)

            lvl_time = pygame.time.get_ticks()
            score = 0
            lvl_score = 0
            heart_score = 0

            player_sprite = pygame.sprite.Group()
            all_enemy = pygame.sprite.Group()
            all_stones = pygame.sprite.Group()
            all_fire = pygame.sprite.Group()
            all_hearts = pygame.sprite.Group()
            all_caves = pygame.sprite.Group()

            player = Player(player_sprite)
            stone = Stone(all_stones)  # первый камень на экране
            game = Game(player, stone, setting.screen)
            cave = Cave(all_caves)

            pause_btn, pause_rect = create_btn(r'images/menu/pause_btn.png', (setting.WINDOW_WIDTH - 140, 15))
            menu_btn, menu_rect = create_btn(r'images/menu/menu_btn.png', (setting.WINDOW_WIDTH - 80, 15))
            exit_btn, exit_rect = create_btn(r'images/menu/exit_btn.png', (setting.WINDOW_WIDTH - 20, 15))

            setting.NEW_GAME = False

        pygame.display.flip()
        clock.tick(setting.FPS)

    pygame.quit()
    setting.db.close()
    exit()


if __name__ == '__main__':
    main()

