import random
import pygame
from pygame import Surface
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()
FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_LIME = (0, 255, 0)

player_move_down = [0, 10]
player_move_right = [10, 0]
player_move_up = [0, -10]
player_move_left = [-10, 0]

player: Surface
player_rect: pygame.Rect
bg_X1: int
bg_X2: int
bg_move: int

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Potuzhniy gusenok")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, random.randint(1500, 3000))
enemies = []

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, random.randint(3000, 5000))
bonuses = []
high_score = 0
score = 0


def init_game():
    global main_display
    global bg
    global bg_X1
    global bg_X2
    global bg_move
    bg_X1 = 0
    bg_X2 = bg.get_width()
    bg_move = 3

    player_size = (182, 76)
    global player
    player = pygame.image.load('player.png').convert_alpha()
    # player.fill(COLOR_WHITE)
    # player_rect = player.get_rect()
    global player_rect
    player_rect = pygame.Rect(0, HEIGHT - 380, *player_size)
    # player_speed = [1, 1]

    global high_score
    try:
        high_score_file = open('highscore.txt', 'r+')
        high_score = high_score_file.read()
        high_score = int(high_score)
        high_score_file.close()
    except:
        high_score = 0


def create_enemy():
    enemy_size = (205, 72)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    #    enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - enemy_size[1]), *enemy_size)
    enemy_move = [random.randint(-16, -6), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus_size = (179, 298)
    bonus = pygame.image.load('bonus.png').convert_alpha()
    #    bonus.fill(COLOR_YELLOW)
    bonus_rect = pygame.Rect(random.randint(0, WIDTH - bonus_size[0]), -bonus_size[1], *bonus_size)
    bonus_move = [0, random.randint(3, 10)]
    return [bonus, bonus_rect, bonus_move]

playing = True
game_is_running = False

while playing:
    FPS.tick(60)

    if not game_is_running:
        init_game()
        game_is_running = True

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            game_is_running = False
            enemies.clear()
            bonuses.clear()
            if score > high_score:
                high_score_file = open('highscore.txt', 'w+')
                high_score_file.write(str(score))
                high_score_file.close()
            score = 0


    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))
    if high_score > score:
        main_display.blit(FONT.render(str(high_score), True, COLOR_LIME), (50, 20))
    else:
        main_display.blit(FONT.render(str(score), True, COLOR_LIME), (50, 20))
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
