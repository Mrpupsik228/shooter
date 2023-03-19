# Створи власний Шутер!

from time import time as timer
from pygame import *
from random import randint
import pygame_menu
import sys


init()

w, h = 700, 500
mw = display.set_mode((w, h))

img_bulet = "bullet.png"
img_hero = "rocket.png"
rel_time = False
num_fire = 0

life = 3
killed = 0
goal = 10
max_lost = 10
score = 0
w, h = 700, 500
mw = display.set_mode((w, h))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (w,h))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.pause()
fire_sound = mixer.Sound("fire.ogg")
font.init()
text1 = font.Font(None,36)
text2 = font.Font(None,80)



win = text2.render("YOU WIN", True,(138,65,5),(43,240,195))

lose =text2.render("LOSE", True,(248,100,30),(199,60,128))
text_name =text2.render("SHOOTER", True,(248,100,30),(199,60,128))
text_play =text2.render("PLAY", True,(248,100,30),(199,60,128))
text_exit =text2.render("EXIT", True,(248,100,30),(199,60,128))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x,size_y ,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x >-85:
            self.rect.x += self.speed


    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

    def fire(self):
        bulet = Bulet(img_bulet,self.rect.centerx,self.rect.top,15,20,-15)
        bulets.add(bulet)


player = Player("rocket.png",200,h-100,80,100,7)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global score
        if self.rect.y > h:
            self.rect.y = -50
            self.rect.x = randint(20,w-100)
            score = score +1

class Bulet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

monsters = sprite.Group()
bulets = sprite.Group()
def respawn_enemy():

        monster = Enemy("ufo.png",randint(20,w-100),-50,80,50,randint(1,2))
        monsters.add(monster)
def start_the_game():
    global score,killed,goal,max_lost,life,num_fire,rel_time
    for i in range(1,10):
        respawn_enemy()

    clock= time.Clock()
    finish = False
    game = True
    while game:

        for e in event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN:
                if e.key == K_UP:
                    if num_fire <5 and rel_time == False:
                        num_fire =+1
                        player.fire()
                    if num_fire >=5 and rel_time == False:
                        last_time = timer()
                        rel_time = True
                    #fire_sound.play()
                    player.fire()

        if not finish:
            mw.blit(background, (0, 0))
            player.update()
            monsters.draw(mw)
            monsters.update()
            bulets.update()

            player.reset()
            text_killed = text1.render("Рахунок 5", str(score),1,(255,0,0))
            mw.blit (text_killed,(20,20))
            bulets.draw(mw)
            text_lost = text1.render("Пропущено"+ str(killed),1,(135,145,240))
            mw.blit (text_lost,(20,45))

            if rel_time:
                now_time = timer()
                if now_time - last_time < 3 :
                    reload = text1.render("WTF"),1 ,(127,211,35)
                    mw.blit(reload,(w//2-50,h-50))

            if sprite.spritecollide(player,monsters,False) or score >= max_lost:
                mw.blit(lose,(150,200))
                time.delay(3000)
                game = True
                finish = True
            collides =sprite.groupcollide(monsters,bulets,True,True)
            for colide in collides:
                killed +=1
                respawn_enemy()

            if killed >= goal:
                finesh = True
                mw.blit(win,(150,200))
  

        else:
            finish = False
            killed = 0
            score = 0 
            for bulet in bulets:
                bulet.kill()
            for monster in monsters:
                monster.kill()
            for i in range(1,10):
                respawn_enemy()
        display.update()
        clock.tick(60)

menu = pygame_menu.Menu('Вітаємо в меню', w,h,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.button('Грати', start_the_game)
menu.add.button('Вийти', pygame_menu.events.EXIT)
menu.mainloop(mw)