
import random
import pygame
from pygame import font
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (33, 152, 25)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
pygame.init()

# Set the width and height of the screen [width, height]
size = (1300, 700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
blue_monster_image = pygame.image.load("monster1.png").convert()
coin_image = pygame.image.load("coin1.png").convert()
lose_image = pygame.image.load("unnamed.png").convert()
click_sound = pygame.mixer.Sound('laser.wav')
collision_sound = pygame.mixer.Sound('explosion.wav')
bullet_image= pygame.image.load("circle.png").convert()
pygame.mixer.music.load('background.wav')
blue_monster_image.set_colorkey(BLACK)
coin_image.set_colorkey(BLACK)
player_image = pygame.image.load("space_man.png").convert()
monster_image = pygame.image.load("monster.png").convert()
background_image = pygame.image.load("galaxy.jpg").convert()
click_sound = pygame.mixer.Sound('laser.wav')
lose_sound = pygame.mixer.Sound('lose.wav')
collision_sound = pygame.mixer.Sound('explosion.wav')
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play()
player_image.set_colorkey(BLACK)
monster_image.set_colorkey(BLACK)

class Player(pygame.sprite.Sprite):
    """ The class is the player-controlled sprite. """
    # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
    def update(self, x,y):
        self.rect.x=x
        self.rect.y=y

class Bullet(pygame.sprite.Sprite):
    # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.y=y
        self.rect.x=x
    def update(self):
        self.rect.x+=5

class Monster(pygame.sprite.Sprite):
    # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()
        self.image = monster_image
        self.rect = self.image.get_rect()
        self.rect.y=y
        self.rect.x=x
    def update(self):
        self.rect.x-=3

class Blue_Monster(pygame.sprite.Sprite):
    # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()
        self.image = blue_monster_image
        self.rect = self.image.get_rect()
        self.rect.y=y
        self.rect.x=x
    def update(self):
        self.rect.x -= random.randrange(3, 7)
        if self.rect.y<5:
            self.rect.y += random.randrange(18, 25)
        elif self.rect.y > 635:
            self.rect.y -= random.randrange(18, 25)
        else:
            self.rect.y += random.randrange(-25, 25)

player = Player(280, 570)
click=0
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)
x_monster=600
y_monster=0
monster_speed=3
x_monster_two=500
y_monster_two=430
monster_speed_two=-3
bullet_list = pygame.sprite.Group()
monster_list = pygame.sprite.Group()
blue_monster_list = pygame.sprite.Group()
new_list=[]
comment_counter=60
shots=0
hits=0
loop_counter=0
time_counter=0
font = pygame.font.SysFont('Calibri', 34, True, False)
font_two = pygame.font.SysFont('Calibri', 20, True, False)
score=0
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    counter=0
    loop_counter+=1
    if loop_counter%415==0 or loop_counter==0:
        for i in range(int(loop_counter/415)+3):
            monster=Monster(random.randrange(1300, 2600),random.randrange(0, 630))
            monster_list.add(monster)
            all_sprites_list.add(monster)

    if loop_counter%900==0:
        monster=Blue_Monster(random.randrange(1300, 2600),random.randrange(0, 630))
        blue_monster_list.add(monster)
        all_sprites_list.add(monster)

    player_position = pygame.mouse.get_pos()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:#if they click, they shoot a circle
            bullet=Bullet(player_position[0]+60, player_position[1]+20)
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)
            click_sound.play()

        player_position = pygame.mouse.get_pos()
        player.update(player_position[0],player_position[1])

    for item in bullet_list:
        item.update()
    for item in monster_list:
        item.update()
    for item in blue_monster_list:
        item.update()

    # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    # --- Drawing code should go here
    screen.blit(background_image, [0, 0])
    if loop_counter<500:
        text = font_two.render("Aliens are trying to attack your home!", True, WHITE)
        screen.blit(text, [510, 250])
        text = font_two.render(
            "Click to shoot them and don't let them get to your home.", True, WHITE)
        screen.blit(text, [420, 290])
        text = font.render("Good luck!", True, WHITE)
        screen.blit(text, [570, 340])

    for bullet in bullet_list:
        if bullet.rect.x>1300:
            bullet_list.remove(bullet)
        blocks_hit_list = pygame.sprite.spritecollide(bullet, monster_list, True)
        if blocks_hit_list:
            bullet_list.remove(bullet)
            collision_sound.play()
            score+=100

    for bullet in bullet_list:
        blue_blocks_hit_list = pygame.sprite.spritecollide(bullet, blue_monster_list, True)
        if blue_blocks_hit_list:
            bullet_list.remove(bullet)
            collision_sound.play()
            score+=300

    bullet_list.draw(screen)
    monster_list.draw(screen)
    blue_monster_list.draw(screen)
    for item in monster_list:
        if item.rect.x<50:
            counter+=1
    for item in blue_monster_list:
        if item.rect.x<50:
            counter+=1

    if counter>0:
        time_counter+=1
        screen.blit(lose_image, [370, 130])
        lose_sound.play()

    if time_counter>220:
        done=True

    x = player_position[0]
    y = player_position[1]
    # Copy image to screen:
    screen.blit(player_image, [x-70, y-70])

    pygame.draw.rect(screen, BLUE, [0, 0, 100, 700], 0)
    text = font.render("HOME", True, WHITE)
    screen.blit(text, [5, 330])
    text = font.render("Score: "+str(score), True, WHITE)
    screen.blit(text, [1050, 10])
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()