import pygame
import random
import sys
import time


W = 600
H = 1000
running = True
player_car_speed = 20
other_car_speed = player_car_speed * 2
Red = (255, 0, 0)
White = (255, 255, 255)
start_text1 = 'Race'
start_text2 = 'by Vinoggradic1'
start_description_text1 = "'enter' to start"
start_description_text2 = "'escape' to quit"
game_over_text = 'Game over'
game_over_description_text1 = "'enter' to restart"
game_over_description_text2 = "'escape' to quit"
start_text1_rect = (130, 100)
start_text2_rect = (140, 200)
game_over_text_rect = (40, 100)
description_text1_rect = (150, 400)
description_text2_rect = (150, 420)
other_car_generate_chance = 98
explosion_animation_blocked = False
Fps = 58
score = 0
scroe_rect = (550, 0)
started = False
game_over = False


pygame.init()
pygame.display.set_caption('Raicing')
pygame.display.set_icon(pygame.image.load('textures/Race.ico'))
screen = pygame.display.set_mode((W, H))
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 100, True, False)
description_font = pygame.font.SysFont('Arial', 25, False, False)
explosion_time = time.time()


class Road(pygame.sprite.Sprite):
    def __init__(self, road_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('textures/Road.png')
        self.rect = self.image.get_rect(topleft=(0, road_y))

    def update(self):
        if not game_over:
            self.rect.y = self.rect.y + player_car_speed
        if self.rect.y == 0:
            self.rect.y = -1000


class Player_car(pygame.sprite.Sprite):
    def __init__(self, player_car_x, player_car_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('textures/player_car.png')
        self.rect = self.image.get_rect(center=(player_car_x, player_car_y))
        self.line = 1

    def update(self):
        if self.rect.colliderect(other_car.rect):
            global game_over
            global started
            global score
            game_over = True
            started = False
            score = 0
            other_car.rect.x = 370
            other_car.rect.y = -200
            
    def turn_left(self):
        if self.line == 1:
            self.rect.x = self.rect.x - 1
            self.line = 0
        if self.line == 2:
            self.rect.x = self.rect.x - 1
            self.line = 1

    def turn_right(self):
        if self.line == 1:
            self.rect.x = self.rect.x + 1
            self.line = 2
        if self.line == 0:
            self.rect.x = self.rect.x + 1
            self.line = 1


class Other_car(pygame.sprite.Sprite):
    def __init__(self, other_car_x, other_car_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('textures/other_car.png')
        self.rect = self.image.get_rect(topleft=(other_car_x, other_car_y))
        self.line = 0
        self.chance = 0

    def update(self):
        if self.chance < other_car_generate_chance or self.chance == other_car_generate_chance:
            self.chance = random.randint(0, 99)
            self.line = random.randint(0, 2)
        elif self.chance > other_car_generate_chance:
            if self.line == 0:
                self.rect.x = 130
                self.rect.y = self.rect.y + other_car_speed
            elif self.line == 1:
                self.rect.x = 250
                self.rect.y = self.rect.y + other_car_speed
            elif self.line == 2:
                self.rect.x = 370
                self.rect.y = self.rect.y + other_car_speed
            if self.rect.y > 1000:
                global score
                score = score + 1
                self.rect.x = 370
                self.rect.y = -200
                self.chance = 0
                self.line = 0


class Explosion(pygame.sprite.Sprite):
    def __init__(self, explosion_x, explosion_y):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load('textures/explosion1.png')
        self.image1_rect = self.image1.get_rect(center=(explosion_x, explosion_y))
        self.image2 = pygame.image.load('textures/explosion2.png')
        self.image2_rect = self.image2.get_rect(center=(explosion_x, explosion_y))

    def update(self):
        global explosion_time
        global explosion_animation_blocked
        if not explosion_animation_blocked:
            screen.blit(self.image1, self.image1_rect)
            if time.time() - explosion_time > 2.0:
                explosion_time = time.time()
                explosion_animation_blocked = True
        elif explosion_animation_blocked:
            screen.blit(self.image2, self.image2_rect)


road = Road(-1000)
player_car = Player_car(300, 850)
other_car = Other_car(300, -200)

roads = pygame.sprite.Group()
roads.add(road)

player_cars = pygame.sprite.Group()
player_cars.add(player_car)

other_cars = pygame.sprite.Group()
other_cars.add(other_car)


def mainloop():
    global game_over
    global started
    global explosion_time
    global explosion_animation_blocked 
    clock.tick(Fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
            if event.key == pygame.K_RETURN:
                if not started and not game_over:
                    started = True
                    game_over = False
                if not started and game_over:
                    started = False
                    game_over = False
            if started and not game_over:
                if event.key == pygame.K_a:
                    player_car.turn_left()
                elif event.key == pygame.K_d:
                    player_car.turn_right()
    roads.draw(screen)
    screen.blit(description_font.render(str(score), True, White), (scroe_rect))
    if not started and not game_over:
        explosion_animation_blocked = False
        start_menu_init()
    if started and not game_over: 
        player_cars.draw(screen)
        player_car.update()
        other_cars.draw(screen)
        other_car.update()
    if not game_over:
        road.update()
    elif game_over:
        explosion = Explosion(player_car.rect.x, player_car.rect.y + 50)
        explosion.update()
        game_over_menu_init()
    pygame.display.flip()


def start_menu_init():
    screen.blit(font.render(start_text1, True, Red), start_text1_rect)
    screen.blit(description_font.render(start_text2, True, Red), start_text2_rect)
    screen.blit(description_font.render(start_description_text1, True, Red), description_text1_rect)
    screen.blit(description_font.render(start_description_text2, True, Red), description_text2_rect)

def game_over_menu_init():
    screen.blit(font.render(game_over_text, True, Red), game_over_text_rect)
    screen.blit(description_font.render(game_over_description_text1, True, Red), description_text1_rect)
    screen.blit(description_font.render(game_over_description_text2, True, Red), description_text2_rect)


while running:
    mainloop()
