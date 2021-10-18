import pygame
from sys import *
import random
from pygame import mixer
from pygame.constants import KEYDOWN
import resource

from resource import ship

#fps
def fps():
    fps = "FPS: " + str(int(clock.get_fps()))
    return fps

#score
score = 0
boss_present = 0

#enemy ship
ship_list = []
boss_list = []
now = 0
dead_ships = []

#bullet
bullet_list = []
e_bullet_list =[]
boss_bullet_list = []
flag = 0

#explosion
explosion_list = []
del_list = []

pygame.init()
mixer.init()
screen = pygame.display.set_mode((500, 900))
background = pygame.image.load('assets/background_space.png').convert()
pygame.font.init()
font = pygame.font.Font('assets/ariel.ttf', 17)
score_font = pygame.font.Font('assets/ariel.ttf', 17)
font_died = pygame.font.Font('assets/ariel.ttf', 28)
died = font_died.render("You died", False, 'White')

clock = pygame.time.Clock()

hero = resource.ship([pygame.mouse.get_pos()[0], 800], resource.hero, 100, 0)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        m_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (m_pos[0] >= 100 and m_pos[0] < 400) and (m_pos[1] >= 150 and m_pos[1] < 250):
                density = 70
                enemy_ammo_hardness = 1
                flag = 1
                boss_hardness = 700
                enemy_health = 50
            elif (m_pos[0] >= 100 and m_pos[0] < 400) and (m_pos[1] >= 400 and m_pos[1] < 500):
                density = 55
                enemy_ammo_hardness = 2
                flag = 1
                boss_hardness = 600
                enemy_health = 75
            elif (m_pos[0] >= 100 and m_pos[0] < 400) and (m_pos[1] >= 650 and m_pos[1] < 750):
                density = 40
                enemy_ammo_hardness = 3
                flag = 1
                boss_hardness = 500
                enemy_health = 100

    screen.blit(background, (0,0))
    screen.blit(resource.easy, (100,150))
    screen.blit(resource.medium, (100, 400))
    screen.blit(resource.hard, (100, 650))
    pygame.display.update()
    if flag == 1:
        break

heal = []
heal_num = 0
#main game
while 1:
    
    #screening fps
    fps_update = font.render(fps(), False, 'White')
    f_score = score_font.render(str("score: "+str(score)), False, 'White')

    #firing and quiting game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            j = resource.object([hero.position[0]+22, 800], resource.bullet_texture2, 20, 25)
            mixer.music.load(resource.sound1)
            mixer.music.set_volume(0.2)
            mixer.music.play()
            bullet_list.append(j)
    
    #spawning enemies
    if now == 0:
        i = resource.ship([random.randint(25,425), -50], resource.enemy[random.randint(0,2)], enemy_health, random.randint(3,7))
        ship_list.append(i)
        now = density
        if score%boss_hardness == 0 and score > 0 and boss_present!=score:
            boss = resource.ship([random.randint(48, 452), -100], resource.boss, 1000, 1)
            boss.ammo_color = resource.bullet_texture_boss2
            boss_present = score
            ship_list.append(boss)
    now -= 1
    if score%2000 == 0 and score > 0 and score!=heal_num:
        h = resource.health()
        heal_num = score
        heal.append(h)

    hero.position[0] = pygame.mouse.get_pos()[0]
    hero.center()[0] = hero.position[0]+hero.width/2
    hero.center()[1] = 800+hero.height/2

    # collision with boundry 
    if hero.position[0] >= 450:
        hero.position[0] = 449
            
    # screening background, fps and score
    screen.blit(background, (0,0))
    screen.blit(fps_update, (438,0))
    screen.blit(f_score, (0,0))
    
    # screening and flying bullet
    for bullet in bullet_list:
        bullet.position[1] -= bullet.speed
        bullet.center()[1] -= bullet.speed 
        screen.blit(bullet.skin, bullet.position)
        
    # blit-ing hero ship after bullet
    screen.blit(hero.skin, hero.position)

    # Heal algorithm
    for h in heal:
        h1 = h.center()[0]
        x2 = hero.center()[0]
        p1 = h.center()[1]
        y2 = hero.center()[1]
        rad_sum = h.radius + hero.radius
        if (abs(x2-h1)<=rad_sum and abs(y2-p1)<=rad_sum) or h.position[1] == 920:
            mixer.music.load(resource.sound5)
            mixer.music.set_volume(1)
            mixer.music.play()
            hero.health = 100
            heal = []
        else:
            h.position[1] += h.speed
            screen.blit(h.skin, h.position)

    #collision and game over
    for index, j in enumerate(ship_list):
        if j.reload == 0 and j.health!=0:
            enemy_bullet = resource.object(j.center(), j.ammo_color, j.speed+7, enemy_ammo_hardness)
            e_bullet_list.append(enemy_bullet)
            mixer.music.load(resource.sound3)
            mixer.music.set_volume(0.1)
            mixer.music.play()
            j.reload = j.dummy

        j.reload -= 1
        j.position[1] += j.speed
        j.center()[1] += j.speed

        x1 = j.center()[0]
        x2 = hero.center()[0]
        y1 = j.center()[1] 
        y2 = hero.center()[1]

        rad_diff = j.radius + hero.radius


        if (abs(x2-x1)<=rad_diff and abs(y2-y1)<=rad_diff):

            hero.health -= 2
            j.health -= 5
            
            # blasting enemy ship on collision with our ship
            if j.health <= 0:
                explosion_list.append([j.position[0], j.position[1], 0])

            if hero.health < 0:
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    screen.blit(died, (190,450))
                    pygame.display.update()
        

        screen.blit(j.skin, j.position)

        for bullet in bullet_list:
            x2 = bullet.center()[0]
            y2 = bullet.center()[1]
            if  (abs(x2-x1)<=rad_diff and abs(y2-y1)<=rad_diff) :  
                
                j.health -= bullet.damage
                score += bullet.damage
                bullet.skin = resource.inv_bullet
                bullet.damage = 0
                if j.position[1]>=900 or j.health<=0:
                    mixer.music.load(resource.sound2)
                    mixer.music.set_volume(5)
                    mixer.music.play()
                    j.health = 0
                    # dead_ships.append(index)
                    explosion_list.append([j.position[0], j.position[1], 0])
    
        
    #screening health bar
    screen.blit(resource.red_line, (50, 885))
    blocks = int(hero.health)
    for i in range (50, 4*blocks + 50, 4):
        screen.blit(resource.green_line, [i, 885])

    try:
        if bullet_list[0].position[1] < 0 and len(bullet_list)>0:
            del bullet_list[0]
    except:
        pass

    # new method to remove gone ships
    for i, j in enumerate(ship_list):
        if j.health <= 0 or j.position[1] >= 900:
            try:
                del ship_list[i]
            except:
                print(j.health)

    for i in e_bullet_list:

        i.position[1] += i.speed
        i.center()[1] += i.speed
        screen.blit(i.skin, i.position)

        x1 = i.center()[0]
        x2 = hero.center()[0]
        y1 = i.center()[1]
        y2 = hero.center()[1]
        rad_diff = i.radius + hero.radius
            
        if (abs(x2-x1)<=rad_diff and abs(y2-y1)<=rad_diff):
            mixer.music.load(resource.sound4)
            mixer.music.set_volume(1)
            mixer.music.play()
            hero.health -= i.damage
            i.skin = resource.inv_bullet
            if hero.health < 0:
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    screen.blit(died, (190,450))
                    pygame.display.update()

        try:
            if i.position[1] >= 900 and len(e_bullet_list)>0:
                print(len(e_bullet_list))
                del e_bullet_list[e_bullet_list.index(i)]
        except:
            pass
    
    for i in explosion_list:
        screen.blit(resource.explosion_img[int(i[2])], [i[0], i[1]])
        i[2] += 0.3
        if int(i[2]) == len(resource.explosion_img):
            del_list.append(i)

    for i in del_list:
        del explosion_list[explosion_list.index(i)]
    del_list = []

    #updating display
    pygame.display.update()
    clock.tick(60)
