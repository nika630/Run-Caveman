import sqlite3

import pygame


pygame.init()


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 889, 500
FPS = 60
LAND = 50
SPEED = 1
LEVEL = 1
SCORE = 0
HEALTH = 3
NEW_GAME = False

BG_UP = r'Backgrounds/background_up.png'
BG_DOWN = r'Backgrounds/background_down.png'

STONE_IMG = [r'images/stones/00.png', r'images/stones/22.png',
             r'images/stones/44.png', r'images/stones/55.png',
             r'images/stones/66.png', r'images/stones/77.png']
STONE_HEIGHT = [29, 43, 26, 53, 54, 61]
STONE_WIGHT = [40, 50, 30, 65, 60, 70]

MENU_IMG = [r'images/menu/play_btn.png', r'images/menu/play_btn_2.png',
            r'images/menu/options_btn.png', r'images/menu/options_btn_2.png',
            r'images/menu/quit_btn.png', r'images/menu/quit_btn_2.png',
            r'images/menu/continue_btn.png', r'images/menu/continue_btn_2.png']
# Персонаж 80 * 80
GO_RIGHT = [r'images/go_right/0.png', r'images/go_right/1.png',
            r'images/go_right/2.png', r'images/go_right/3.png',
            r'images/go_right/4.png', r'images/go_right/5.png',
            r'images/go_right/6.png', r'images/go_right/7.png']
GO_LEFT = [r'images/go_left/0.png', r'images/go_left/1.png',
           r'images/go_left/2.png', r'images/go_left/3.png',
           r'images/go_left/4.png', r'images/go_left/5.png',
           r'images/go_left/6.png', r'images/go_left/7.png']
PLAYER_JUMP = [r'images/jump/0.png', r'images/jump/1.png',
               r'images/jump/2.png', r'images/jump/3.png',
               r'images/jump/4.png', r'images/jump/5.png',
               r'images/jump/6.png', r'images/jump/7.png',
               r'images/jump/8.png', r'images/jump/9.png']

ENEMY = [r'images/enemy/0.png', r'images/enemy/1.png',
         r'images/enemy/22.png', r'images/enemy/3.png',
         r'images/enemy/4.png']

FIRE = [r'images/fire/0.png', r'images/fire/1.png', r'images/fire/2.png']
HEALTH_IMG = [r'images/other/heart.png']
LVL_SCORE = 300

screen = pygame.display.set_mode(WINDOW_SIZE)
icon = pygame.image.load(r'Backgrounds/icon.png').convert_alpha()
pygame.display.set_icon(icon)

db = sqlite3.connect('db/statistic.db')
sql = db.cursor()


def new_db():
    sql.execute("""CREATE TABLE IF NOT EXISTS Hearts(
                count INT
            )""")
    sql.execute("""DELETE FROM Hearts""")
    sql.execute("""INSERT INTO Hearts VALUES(?) """, (3,))

    sql.execute('''CREATE TABLE IF NOT EXISTS Time (count INT)''')
    sql.execute('''CREATE TABLE IF NOT EXISTS User (
                    score INT,
                    level INT)''')
    db.commit()


def lvl_up():  # изменение скорости на новом уровне игры
    global SPEED, LEVEL
    SPEED += 1
    LEVEL += 1


def new_game():
    global NEW_GAME, SPEED, LEVEL
    NEW_GAME = True
    sql.execute("""INSERT INTO Hearts VALUES(?) """, (3,))
    SPEED = 1
    LEVEL = 1

