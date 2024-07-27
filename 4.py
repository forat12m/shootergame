from pygame import *
from random import randint
# load functions for working with fonts separately
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)

#background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# we need these pictures:
img_back = "galaxy.jpg" # game background
 
img_bullet = "bullet.png" # bullet
img_hero = "rocket.png" # character
img_enemy = "ufo.png" # enemy
 
score = 0 # ships hit
goal = 10 # how many ships need to be hit to win
lost = 0 # ships missed
max_lost = 3 # lost if this many missed
 
# parent class for other sprites
class GameSprite(sprite.Sprite):
  # class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # We call the class constructor (Sprite):
        sprite.Sprite.__init__(self)

        # each sprite must store an image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # each sprite must store the rect property it is inscribed in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # method that draws the character in the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# main player class
class Player(GameSprite):
    # method for controlling the sprite with keyboard arrows
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # the "fire" method (use the player's place to create a bullet there)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# enemy sprite class   
class Enemy(GameSprite):
    # enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost
        # disappears if it reaches the edge of the screen
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 
# bullet sprite class   
class Bullet(GameSprite):
    # enemy movement
    def update(self):
        self.rect.y += self.speed
        # disappears if it reaches the edge of the screen
        if self.rect.y < 0:
            self.kill()
 
# Create the window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
# creating a group of enemy sprites
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 
bullets = sprite.Group()
 
# the "game over" variable: as soon as it is True, the sprites stop working in the main loop
finish = False
# Main game loop:
run = True # the flag is cleared with the close window button
while run:
    # the press the Close button event
    for e in event.get():
        if e.type == QUIT:
            run = False
        # press on the space bar event - the sprite fires
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
 
  # the game itself: sprite actions, checking the rules of the game, redrawing
    if not finish:
        # refresh background
        window.blit(background,(0,0))

        # writing text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # producing sprite movements
        ship.update()
        monsters.update()
        bullets.update()

        # updating them at a new location on each iteration of the loop
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
 
        # bullet-monster collision check (both monster and bullet disappear upon touching)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # this loop will be repeated as many times as monsters are killed
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # possible loss: missed too many or the character collided with the enemy
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True # lost, set the background and no more sprite control.
            window.blit(lose, (200, 200))

        # win check: how many points did you score?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    # the loop runs every 0.05 seconds
    time.delay(50)
