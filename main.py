import pygame
import math
import random
from pygame import mixer 
import time
import numpy as np

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('background2.jpg')

pygame.display.set_caption("Ну, погоди! — Волк ловит яйца")

mixer.music.load('kuryatnik.mp3')
mixer.music.play(-1)  

#main menu
mainmenu = np.array([["->","Начать игру"],["__","Лучший результат"],["__","Выйти"]])
start_font = pygame.font.Font('freesansbold.ttf', 24)

def show_explanation():
    explanation = start_font.render("Используйте ↑/↓ для переключения и ENTER для выбора ", True, (255,128,0))
    screen.blit(explanation, (50, 50))


try:
    with open('highscore.dat') as high_score_file:
        high_score = int(high_score_file.read())
except FileNotFoundError:
    high_score = 0


chickenImg = pygame.image.load('chicken.png')
chickenX0 = 50
chickenY = 40
chickenX = []
for i in range(9):
    chickenX.append(chickenX0 + i * 80)

def chicken():
    for i in range(9):
        screen.blit(chickenImg, (chickenX[i], chickenY))





eggImg = pygame.image.load('egg.png')
eggX = [random.choice(chickenX)+25]
eggY = [chickenY + 40]


def egg(x, y):
    screen.blit(eggImg, (x, y))


wolfIm = pygame.image.load('wolf2.png')
wolfX = 450
wolfY = 485
wolfX_change = 0


def wolf(x, y):
    screen.blit(wolfIm, (x, y))


def isCaught(eggX, eggY, wolfX, wolfY):
    distance = math.sqrt(math.pow(eggX - wolfX - 8, 2) + math.pow(eggY - wolfY + 16, 2))
    if distance < 8:
        return True


font = pygame.font.Font('freesansbold.ttf', 20)

missed_scoreX = 10
missed_scoreY = 10
caught_scoreX = 400
caught_scoreY = 10
caught_score_value = 0
missed_score_value = 0

def show_scores(x, y, x2, y2):
    missed_score = font.render("Количество пропущенных яиц: " + str(abs(missed_score_value)), True, (255, 0, 0))
    caught_score = font.render("Количество собранных яиц: " + str(caught_score_value), True, (0, 255, 0))
    screen.blit(missed_score, (x, y))
    screen.blit(caught_score, (x2, y2))


over_font = pygame.font.Font('freesansbold.ttf', 64)
over_font_small = pygame.font.Font('freesansbold.ttf', 14)


def game_over():
    over_txt = over_font.render("ИГРА ЗАКОНЧЕНА", True, (255, 0, 0))
    screen.blit(over_txt, (200, 150))
    over_txt_small = over_font_small.render("*В главное меню через 5 секунд", True, (10, 10, 10))
    screen.blit(over_txt_small, (220, 250))


def game_start():
    global eggY, wolfX_change, wolfX, eggX, caught_score_value, missed_score_value, high_score
    caught_score_value = 0
    missed_score_value = 0
    initial_speed = 0.75
    speed_slope = .05
    eggX = [random.choice(chickenX) + 25]
    eggY = [chickenY + 40]
    egg_num = 1
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill((0, 0, 100))
        screen.blit(background, (0, 0))
        for i in range(egg_num):
            eggY[i] += (initial_speed + speed_slope * caught_score_value)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    wolfX_change = -8
                if event.key == pygame.K_RIGHT:
                    wolfX_change = 8
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.KEYUP:  
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    wolfX_change = 0

        chicken()
        for i in range(egg_num):
            egg(eggX[i], eggY[i])

        if eggY[-1] >= (chickenY + 150):
            egg_num += 1
            eggX.append(random.choice(chickenX) + 25)
            eggY.append(chickenY + 40)
            egg(eggX[-1], eggY[-1])


        if isCaught(eggX[0], eggY[0], wolfX, wolfY):
            eggY.pop(0)
            eggX.pop(0)
            egg_num -= 1
            caught_score_value += 1
            print("количество пойманных яиц", caught_score_value)
            caught_egg_sound = mixer.Sound('eggcaught.mp3')
            caught_egg_sound.play()


        if eggY[0] >= 540:
            if abs(wolfX - eggX[0] + 8) > 32:
                missed_score_value -= 1
                print("количество пропущенных яиц", missed_score_value)
                missed_egg_sound = mixer.Sound('eggdrop.wav')
                missed_egg_sound.play()
                eggY.pop(0)
                eggX.pop(0)
                egg_num -= 1
                if missed_score_value <= -10:
                    game_over()
                    pygame.display.update()
                    print(f"КОНЕЦ ИГРы: количество собранных яиц {caught_score_value}")
                    time.sleep(5)
                    break

            else:
                eggY.pop(0)
                eggX.pop(0)
                egg_num -= 1
                caught_score_value += 1
                print("количество пойманных яиц", caught_score_value)
                caught_egg_sound = mixer.Sound('eggcaught.mp3')
                caught_egg_sound.play()


        wolfX += wolfX_change
        if wolfX <= 0:
            wolfX = 0
        elif wolfX >= 736:
            wolfX = 736

        wolf(wolfX, wolfY)


        show_scores(missed_scoreX, missed_scoreY, caught_scoreX, caught_scoreY)


        pygame.display.update()
        clock.tick(60)
    if caught_score_value > high_score:
        high_score = caught_score_value
        high_score_write = open('highscore.dat', 'w')
        high_score_write.write("%s" %high_score)
        high_score_write.close()


def highscore():
    screen.fill((100, 20, 23))
    screen.blit(background, (0, 0))
    h_score = start_font.render("Ваш наивысший результат: " + str(abs(high_score)), True, (255,128,0))
    screen.blit(h_score, (60, 80))
    over_txt_small = over_font_small.render("*В главное меню через 5 секунд", True, (10, 10, 10))
    screen.blit(over_txt_small, (220, 250))
    pygame.display.update()
    time.sleep(5)



def main_menu():
    intro = True
    menu_clock = pygame.time.Clock()
    navigation_sound = mixer.Sound('click.wav')
    while intro:
        screen.blit(background, (0, 0))

        show_explanation()

        option1 = start_font.render("{}".format(mainmenu[0]), True, (255,128,0))
        screen.blit(option1, (50, 450))
        option2 = start_font.render("{}".format(mainmenu[1]), True, (255,128,0))
        screen.blit(option2, (50, 500))
        option3 = start_font.render("{}".format(mainmenu[2]), True, (255,128,0))
        screen.blit(option3, (50, 550))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    mainmenu[:,0] = np.roll(mainmenu[:,0],-1)
                    navigation_sound.play()
                elif event.key == pygame.K_DOWN:
                    mainmenu[:,0] = np.roll(mainmenu[:,0],1)
                    navigation_sound.play()
                elif event.key == pygame.K_RETURN:
                    navigation_sound.play()
                    if mainmenu[0, 0] == "->":
                        print("начало игры")
                        game_start()
                    elif mainmenu[1, 0] == "->":
                        highscore()
                    elif mainmenu[2, 0] == "->":
                        print("Выход")
                        intro= False
                        break
        menu_clock.tick(30)

main_menu()