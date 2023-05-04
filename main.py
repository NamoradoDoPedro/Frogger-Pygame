import pygame
from random import randint
from pygame.locals import *
from sys import exit

pygame.display.set_caption("Frog Test") 
v = pygame.math.Vector2
clock = pygame.time.Clock()
number = 13
pygame.init()
FPS = 60
class windowInfo:
    def __init__(self):
        self.Dimension = v(300,600)
window = windowInfo()
display = pygame.display.set_mode(window.Dimension)  
aggregator = 1

class frogInfo:
    def __init__(self):
        self.Position = v(140,540)
        self.Dimension = v(20,20)
        self.Lifes = 3
        self.Score = 0
        self.Velocity = self.Dimension.x

    def move(self):
        key = pygame.key.get_pressed()

        if key[K_UP] and self.Lifes > 0:
            self.Position.y = self.Position.y - self.Velocity
        if key[K_DOWN] and self.Lifes > 0 and self.Position.y < window.Dimension.y - self.Dimension.x:
            self.Position.y = self.Position.y + self.Velocity
        if key[K_LEFT] and self.Lifes > 0 and self.Position.x > 0:
            self.Position.x = self.Position.x - self.Velocity
        if key[K_RIGHT] and self.Lifes > 0 and self.Position.x < window.Dimension.x - self.Dimension.x:
            self.Position.x = self.Position.x + self.Velocity

    def resetPos(self):
        self.Position = v(140,540)

    def reset(self):
        self.Position = v(140,540)
        self.Dimension = v(20,20)
        self.Lifes = 3
        self.Score = 0
frog = frogInfo()

class carInfo:
    def __init__(self, x, X):
        self.Position = v(x,0)
        self.Dimension = v(X,frog.Dimension.y)

cars = list()
cars.append(carInfo(30,50))  #1
cars.append(carInfo(130,50)) #1
cars.append(carInfo(230,50)) #1

cars.append(carInfo(35,70))  #2
cars.append(carInfo(185,70)) #2

cars.append(carInfo(20,40))  #3
cars.append(carInfo(130,40)) #3
cars.append(carInfo(240,40)) #3

cars.append(carInfo(50,30))  #4
cars.append(carInfo(130,30)) #4
cars.append(carInfo(310,30)) #4

cars.append(carInfo(20,80))  #5
cars.append(carInfo(200,80)) #5

def create_roads():
    result = list()
    for count in range(5):
        randomizer = randint(0,4)

        while randomizer in result and count > 0:
            randomizer = randint(0,4)

        result.append(randomizer)
        h = (120, 200, 280, 360, 440)
        for i in range(number):
                if randomizer == 0 and -1 < i < 3:
                    cars[i].Position.y = h[count]

                elif randomizer == 1 and 2 < i < 5:
                    cars[i].Position.y = h[count]

                elif randomizer == 2 and 4 < i < 8:
                    cars[i].Position.y = h[count]

                elif randomizer == 3 and 7 < i < 11:
                    cars[i].Position.y = h[count]

                elif randomizer == 4 and 10 < i < 13:
                    cars[i].Position.y = h[count]
create_roads()

def load():
    display.fill((0,0,0))

    carsHitbox = list()
    for i in range(number):
        carsHitbox.append(pygame.draw.rect(display, (200,10,10), (cars[i].Position,cars[i].Dimension))) #cars[0] Hitboxes
    frogHitbox = pygame.draw.rect(display, (10,200,10), (frog.Position,frog.Dimension)) #frog Hitbox

    for i in range(number):
        pygame.draw.rect(display, (200,10,10), (cars[i].Position,cars[i].Dimension)) #cars[0] Draw
    pygame.draw.rect(display, (10,200,10), (frog.Position,frog.Dimension)) #Frog Draw

    global aggregator
    gv = list()
    gv.append(1.5*aggregator)
    gv.append(3.5*aggregator)
    gv.append(3.0*aggregator)
    gv.append(2.4*aggregator)
    gv.append(2.2*aggregator)

    for i in range(number):
        if i < 3:
            cars[i].Position.x = cars[i].Position.x - gv[0]
        elif i < 5:
            cars[i].Position.x = cars[i].Position.x - gv[1]
        elif i < 8:
            cars[i].Position.x = cars[i].Position.x - gv[2]
        elif i < 11:
            cars[i].Position.x = cars[i].Position.x - gv[3]
        else:
            cars[i].Position.x = cars[i].Position.x - gv[4]

        if cars[i].Position.x < -cars[i].Dimension.x:
            cars[i].Position.x = window.Dimension.x
        if cars[i].Position.x < -cars[i].Dimension.x:
            cars[i].Position.x = window.Dimension.x

    if frog.Position.y < 0:
            frog.Position.y = 580
            frog.Score += 1
            create_roads()
            if aggregator < 2:
                aggregator = aggregator + 0.1

    for i in range(number):
        if frogHitbox.colliderect(carsHitbox[i]):
            frog.resetPos()
            frog.Lifes -= 1

    if frog.Lifes == 0:
        aggregator = 5

def show_score():
    Font = pygame.font.get_default_font()
    Font_sys = pygame.font.SysFont(Font, 30)
    Game_Over_Font_sys = pygame.font.SysFont(Font, 70)
    Text_Player_Lifes = Font_sys.render("Lifes: "+str(frog.Lifes),True,(255,240,240))  
    display.blit(Text_Player_Lifes,(200,5))
    Text_Player_Points = Font_sys.render("Score: "+str(frog.Score),True,(255,240,240))
    display.blit(Text_Player_Points,(200,28))

    if frog.Lifes == 0:
        Text_Game_Over = Game_Over_Font_sys.render("GAME OVER",True,(255,240,240))
        display.blit(Text_Game_Over,(0,147))
        Text_Restart = Font_sys.render("Press 'r' for restart",True,(255,240,240))
        display.blit(Text_Restart,(55,241))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            frog.move()

            if key[K_r]:
                create_roads()
                frog.reset()
                aggregator = 1
    load()
    show_score()
    clock.tick(FPS)
    pygame.display.update()
