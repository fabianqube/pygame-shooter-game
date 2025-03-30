#Создай собственный Шутер!

from pygame import *
from random import randint

win_height = 700
win_width = 900

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, direction = None):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = direction

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self, speed):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 10:
            self.rect.x -= speed
        if keys[K_RIGHT] and self.rect.x < 820:
            self.rect.x += speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx -9, self.rect.top, 10, 20, 20)
        bullets_group.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, speed):
        super().__init__(player_image, player_x, player_y)
        self.speed = speed
    def update(self):
        global missed_counter
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(10, win_width)
            missed_counter += 1

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, speed, x_size, y_size):
        super().__init__(player_image, player_x, player_y)
        self.speed = speed
        self.x_size = x_size
        self.y_size = y_size
        self.image = transform.scale(image.load(player_image), (self.x_size, self.y_size))
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

spaceship = Player('rocket.png', 450, 600)
ufo_group = sprite.Group()
bullets_group = sprite.Group()
for _ in range(5):
    speed = randint(1,3)
    x = randint(10, win_width-30)
    ufo = Enemy('ufo.png', x, 0, speed)
    ufo_group.add(ufo)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
bullet_sound = mixer.Sound('fire.ogg')

window = display.set_mode((win_width, win_height))
display.set_caption('Shooter Game')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
clock = time.Clock()
FPS = 60
run = True
run_2 = True
ufo_counter = 0
missed_counter = 0
font.init()
text = font.Font(None, 50)



while run:
    window.blit(background, (0, 0))
    events = event.get()
    for e in events:
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                spaceship.fire()
                bullet_sound.play()
    collides = sprite.groupcollide(ufo_group, bullets_group, True, True)
    for _ in collides:
        ufo_counter += 1
        speed = randint(1,3)
        x = randint(10, win_width-30)
        ufo = Enemy('ufo.png', x, 0, speed)
        ufo_group.add(ufo)
    if missed_counter == 10 or ufo_counter == 10:
        run = False
    kills_counter = text.render(f"Ufo's killed:{ufo_counter}", True, (250, 248, 247))
    missed = text.render(f"Ufo's missed:{missed_counter}", True, (250, 248, 247))
    window.blit(kills_counter, (0,0))
    window.blit(missed, (0,50))
    bullets_group.draw(window)
    bullets_group.update() 
    ufo_group.draw(window)
    ufo_group.update()
    spaceship.reset()
    spaceship.update(10)
    display.update()
    clock.tick(FPS)
while run_2:
    window.blit(background, (0, 0))
    events = event.get()
    for e in events:
        if e.type == QUIT:
            run_2 = False
    if ufo_counter == 10:
        win = text.render('You won', True, (250, 248, 247))
        window.blit(win, (350, 450))
    if missed_counter == 10:
        lose = text.render('You lost', True, (250, 248, 247))
        window.blit(lose, (350, 450))
    display.update()
    clock.tick(FPS)
    
