import pygame, random
from pygame.locals import *

SCREEN_WIDTH = 867
SCREEN_HEIGHT = 620
CAR_WIDTH = 100
CAR_HEIGHT = 200
LIMIT_LEFT = 195
LIMIT_RIGHT = 670
GAME_SPEED = 5
CAR_SPEED = 10
GAME_DISTANCE = 300

class Track(pygame.sprite.Sprite):
    def __init__(self, ypos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Track.png')
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH,SCREEN_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = ypos

        

    def update(self):
        self.rect[1] += GAME_SPEED

class CarPlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('Image-Car.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (CAR_WIDTH,CAR_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2 - 20
        self.rect[1] = SCREEN_HEIGHT - CAR_HEIGHT - 20
    
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

    def move_up(self):
        self.rect[1] -= CAR_SPEED

    def move_low(self):
        self.rect[1] += CAR_SPEED

    def move_left(self):
        self.rect[0] -= CAR_SPEED

    def move_right(self):
        self.rect[0] += CAR_SPEED

    

class CarOpponent(pygame.sprite.Sprite):
    def __init__(self, ypos):
        pygame.sprite.Sprite.__init__(self)

        self.images = ['Image-Car-Opp1.png','Image-Car-Opp2.png','Image-Car-Opp3.png']

        self.image = pygame.image.load(self.images[random.randint(0,2)]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (CAR_WIDTH, CAR_HEIGHT))
        self.image = pygame.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()
        self.positionsx = [LIMIT_LEFT,360,LIMIT_RIGHT-CAR_WIDTH]
        self.rect[0] = self.positionsx[random.randint(0,2)]
        self.rect[1] = ypos
    
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[1] += CAR_SPEED

def is_off_screen(sprite):
   
    return sprite.rect[1] > SCREEN_HEIGHT

pygame.init()
 
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("PLAY CAR")

track_group = pygame.sprite.Group()
for i in range(2):
    track = Track(i * -(SCREEN_HEIGHT))
    track_group.add(track)

car_opponent_group = pygame.sprite.Group()
for i in range(2):
    car_opponent = CarOpponent(-GAME_DISTANCE * i - 400)
    car_opponent_group.add(car_opponent)

car_player_group = pygame.sprite.Group()
car_player = CarPlayer()
car_player_group.add(car_player)

delay = pygame.time.Clock()

while True:
    delay.tick(20)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
       
    comandos = pygame.key.get_pressed()
    if comandos[pygame.K_UP] and (car_player.rect[1] - GAME_SPEED > 0):
        car_player.move_up()
    elif comandos[pygame.K_DOWN] and (car_player.rect[1] + CAR_HEIGHT + GAME_SPEED < SCREEN_HEIGHT):
        car_player.move_low()
    elif comandos[pygame.K_RIGHT] and (car_player.rect[0] + CAR_WIDTH + GAME_SPEED < LIMIT_RIGHT):
        car_player.move_right()
    elif comandos[pygame.K_LEFT] and (car_player.rect[0] - GAME_SPEED > LIMIT_LEFT):
        car_player.move_left()

    if(is_off_screen(track_group.sprites()[0])):
        track_group.remove(track_group.sprites()[0])
        new_track = Track(-SCREEN_HEIGHT - 10)
        track_group.add(new_track)

    if(is_off_screen(car_opponent_group.sprites()[0])):
        car_opponent_group.remove(car_opponent_group.sprites()[0])
        new_car_opponent = CarOpponent(-GAME_DISTANCE)
        car_opponent_group.add(new_car_opponent)
    
    track_group.update()
    track_group.draw(screen)

    car_opponent_group.update()
    car_opponent_group.draw(screen)

    car_player_group.update()
    car_player_group.draw(screen)

    pygame.display.update()
    
    if pygame.sprite.groupcollide(car_player_group, car_opponent_group, False, False, pygame.sprite.collide_mask):
        
        input()
        break
        