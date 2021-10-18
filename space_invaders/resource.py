from pygame import *
import pygame
import random

from pygame import mixer

bullet_texture1 = pygame.Surface((5,10))                                                                                #creating bullet texture
bullet_texture1.fill('Red')

bullet_texture2 = pygame.Surface((5, 10))
bullet_texture2.fill("Skyblue")

bullet_texture3 = pygame.Surface((5, 10))
bullet_texture3.fill("green")

bullet_texture4 = pygame.Surface((5, 10))
bullet_texture4.fill("Purple")

bullet_texture_boss1 = pygame.Surface((5, 20))
bullet_texture_boss1.fill("Orange")

bullet_texture_boss2 = pygame.Surface((5, 20))
bullet_texture_boss2.fill("red")

inv_bullet = pygame.Surface((5, 10))
inv_bullet.fill("Black")

#class ship
class ship:
    def __init__(self, position, skin, health, speed):
        self.health = health
        self.position = position
        self.skin = skin
        self.speed = speed
        self.ammo_color = [bullet_texture1, bullet_texture2, bullet_texture3, bullet_texture4, bullet_texture_boss2][random.randint(0, 3)]
        self.reload = random.randint(50, 70)
        self.dummy = self.reload
        self.height = self.skin.get_height()
        self.width = self.skin.get_width()
        self.radius = int((self.width)/2)

    def center(self):
        return [int(self.position[0]+int(self.width/2)), int(self.position[1]+int(self.height/2))]
        

#class bullet
class object:

    def __init__(self, position, skin, speed, damage):
        self.skin = skin
        self.position = position
        self.speed = speed
        self.damage = damage
        self.height = self.skin.get_height()
        self.width = self.skin.get_width()
        self.radius = int(self.width/2)

    def center(self):
        return [int(self.position[0]+int(self.width/2)), int(self.position[1]+int(self.height/2))]

class health:
    def __init__(self):
        self.heal = 100
        self.position = [random.randint(10, 490), -20]
        self.speed = 5
        self.skin = pygame.image.load("assets/health.png")
        self.height = self.skin.get_height()
        self.width = self.skin.get_width()
        self.radius = int(self.width/2)
    
    def center(self):
        return [int(self.position[0]+int(self.width/2)), int(self.position[1]+int(self.height/2))]
    
mixer.init()

hero = pygame.image.load('assets/hero.png')
enemy1 = pygame.image.load('assets/enemy1.png')
enemy2 = pygame.image.load('assets/enemy2.png')
enemy3 = pygame.image.load('assets/enemy3.png')
boss = pygame.image.load('assets/boss.png')
super_hero = pygame.image.load('assets/boss.png')
planet1 = pygame.image.load('assets/planet1.png')
planet2 = pygame.image.load('assets/planet2.png')
astroid = pygame.image.load('assets/astroid.png')
red_line = pygame.image.load('assets/red_line.png')
green_line = pygame.image.load('assets/green_line.png')
easy = pygame.image.load('assets/button1.png')
medium = pygame.image.load('assets/button2.png')
hard = pygame.image.load('assets/button3.png')
exp1 = pygame.image.load('assets/exp1.png')
exp2= pygame.image.load('assets/exp2.png')
exp3 = pygame.image.load('assets/exp3.png')
exp4 = pygame.image.load('assets/exp4.png')
exp5 = pygame.image.load('assets/exp5.png')
exp6 = pygame.image.load('assets/exp6.png')
sound1 = "assets/sounds/gunfire.mp3"
sound2 = "assets/sounds/explosion.wav"
sound3 = "assets/sounds/enemy_gunfire.mp3"
sound4 = "assets/sounds/damage.mp3"
sound5 = "assets/sounds/heal.wav"
explosion_img = [exp1, exp2, exp3, exp4, exp5, exp6]
enemy = [enemy1, enemy2, enemy3]