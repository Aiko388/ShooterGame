#Create your own shooter

from pygame import *
from time import time as timer
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, width, height, speed, asteroid = False):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.asteroid = asteroid

    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('boom.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

from random import randint
    

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(60, win_height - 80)
            self.rect.y = 0
            self.speed = randint(1,2)
            if self.asteroid == False:
                lost += 1 

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bulletsenemy.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        elif self.rect.y > win_height:
            self.kill()

win_width = 700
win_height = 500
back = transform.scale(image.load('Peak.jpg'), (win_width, win_height))
window = display.set_mode((win_width, win_height))
display.set_caption('PERSONHUZZ 🤑🤑')

mixer.init()
mixer.music.load('Last Surprise.mp3')
mixer.music.play()

game = True
finish = False
clock = time.Clock()

ship = Player('Akechers.jpg', 5, win_height - 100, 80, 100, 6)

bullets = sprite.Group()
bulletsenemy = sprite.Group()

monsters = sprite.Group()
for i in range(5):
    m = Enemy('Shido.jpeg', randint(80, win_width -80), 0, 80, 50, randint(1, 2))
    monsters.add(m)

asteroids = sprite.Group()
for i in range(3):
    m = Enemy('asteroid.png', randint(80, win_width -80), 0, 80, 50, randint(1, 2), True)
    monsters.add(m)

lost = 0
score = 0
life = 3

font.init()
font1 = font.Font(None, 36)

wait = 0

fire_sound = mixer.Sound('fire.ogg')

rel_time = False
num_fire = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if finish != True:
        window.blit(back, (0,0))

        text_score = font1.render('Score: '+ str(score), True, (255,255,255))
        window.blit(text_score, (15, 15))

        text_lost = font1.render('Missed: '+ str(lost), True, (255,255,255))
        window.blit(text_lost, (15, 50))

        text_life = font1.render('Life: '+ str(life), True, (255,255,255))
        window.blit(text_life, (win_width-80, 15))

        if wait == 0:
            wait = 100
            for m in monsters:
                fire = randint(0,1)
                if fire == 1:
                    m.fire()
        else:
            wait -= 1       

        ship.update()
        monsters.update()
        bullets.update()
        bulletsenemy.update()
        asteroids.update()
        
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        bulletsenemy.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now = timer()
            if now - last_time < 3:
                reload = font1.render('Wait, reload...', True, (255, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('Shido.jpeg', randint(80, win_width - 80), -40, 50, 50, randint(1, 5))
            monsters.add(monster)

        if score >= 10:
            text_win = font1.render('YOU WIN!', True, (255, 255, 0))
            window.blit(text_win, (win_width/2 - 80, win_height/2))
            finish = True
        
        if sprite.spritecollide(ship, monsters, True) or sprite.spritecollide(ship, bulletsenemy, True) or sprite.spritecollide(ship, asteroids, True):
            life -= 1

        if lost >= 3 or life <= 0:
            text_win = font1.render('YOU LOSE!', True, (255,0,0))
            window.blit(text_win, (win_width/2 - 80, win_height/2))
            finish = True



    display.update()
    clock.tick(60)
