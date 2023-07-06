import pygame as pg
from pygame import Vector2 as v
from random import choice as c, randint as r
from pygame.locals import *
from sys import exit


class Display:
    dimension = v(300, 600)
    display = pg.display.set_mode(dimension)
    title = pg.display.set_caption("Frog Test")


class Frog:
    def __init__(self):
        self.position = v(140, 540)
        self.dimension = v(20, 20)
        self.velocity = v(self.dimension.x, self.dimension.y)
        self.lifes = 3
        self.score = 0
        self.color = (10, 200, 10)

    def move(self):
        if self.lifes > 0:
            key = pg.key.get_pressed()
            if key[K_UP]:
                self.position.y -= self.velocity.y

            if key[K_DOWN] and self.position.y < Display.dimension.y - self.dimension.x:
                self.position.y += self.velocity.y

            if key[K_LEFT] and self.position.x > 0:
                self.position.x -= self.velocity.x

            if key[K_RIGHT] and self.position.x < Display.dimension.x - self.dimension.x:
                self.position.x += self.velocity.x

    def died(self):
        self.position = v(140, 540)
        self.lifes -= 1

    def scored(self) -> bool:
        if self.position.y < 0:
            self.position.y = 580
            self.score += 1
            return True
        else:
            return False

    def reset(self):
        self.position = v(140, 540)
        self.dimension = v(20, 20)
        self.lifes = 3
        self.score = 0


class Car:
    def __init__(self, x, y, X, Y, vel, direction):
        self.position = v(x, y)
        self.dimension = v(X, Y)
        self.velocity = v(vel, 0)
        self.color = (200, 10, 10)
        self.direction = direction

    def move(self, aggregator):
        if self.direction:
            self.position.x -= self.velocity.x * aggregator
            if self.position.x < -self.dimension.x:
                self.position.x = Display.dimension.x
        else:
            self.position.x += self.velocity.x * aggregator
            if self.position.x > Display.dimension.x:
                self.position.x = -self.dimension.x


class Game:
    def __init__(self):
        self._aggregator = 1
        self._frog = Frog()
        self._cars = list()
        self._cached = list()
        self._paused = False
        self._create_roads()

    def update(self):
        Display.display.fill((0, 0, 0))
        self._show_score()
        carsHitbox = [pg.draw.rect(Display.display, car.color,
                                   (car.position, car.dimension)) for car in self._cars]
        frogHitbox = pg.draw.rect(Display.display, self._frog.color,
                                  (self._frog.position, self._frog.dimension))

        for car in self._cars:
            car.move(self._aggregator)
        self.move()

        if self._frog.scored():
            self._create_roads()
            self._aggregator = self._aggregator + \
                0.1 if self._aggregator < 2 else self._aggregator

        for carHitbox in carsHitbox:
            if frogHitbox.colliderect(carHitbox):
                self._frog.died()

        self._aggregator = 5 if self._frog.lifes == 0 else self._aggregator

        pg.display.update()

    def move(self) -> None:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                key = pg.key.get_pressed()
                self._frog.move()

                if key[K_r]:
                    self.reset()

                if key[K_SPACE]:
                    self.pause()

    def reset(self):
        self._create_roads()
        self._frog.reset()
        self._aggregator = 1

    def pause(self):
        if not self._paused:
            for car in self._cars:
                self._cached.append(car.velocity)
                car.velocity = v(0, 0)
            self._frog.velocity = v(0, 0)
            self._paused = True
        else:
            for i, car in enumerate(self._cars):
                car.velocity = self._cached[i]
            self._frog.velocity = v(
                self._frog.dimension.x, self._frog.dimension.y)
            self._paused = False
            self._cached.clear()

    def _create_roads(self):
        self._cars.clear()
        for i, h in enumerate((120, 200, 280, 360, 440)):
            q = r(2, 3)
            a = r(12, 30)/10
            x = r(50, 90) if q == 2 else r(40, 60)
            d = c([True, False])
            g = r(x+int(x/3), Display.dimension.x - x * q)
            for i in range(q):
                self._cars.append(Car(i*g, h, x, self._frog.dimension.y, a, d))

    def _show_score(self):
        FONT = pg.font.get_default_font()
        WHITE = (255, 255, 255)

        SysFont = pg.font.SysFont(FONT, 30).render
        Text_Player_Lifes = SysFont(f"lifes: {self._frog.lifes}", True, WHITE)
        Text_Player_Points = SysFont(f"score: {self._frog.score}", True, WHITE)

        Display.display.blit(Text_Player_Lifes, (200, 5))
        Display.display.blit(Text_Player_Points, (200, 28))

        if self._frog.lifes == 0:
            Text_Game_Over = pg.font.SysFont(FONT, 70).render(
                "GAME OVER", True, WHITE)

            Text_Restart = SysFont(
                "Press 'r' for restart", True, WHITE)

            Display.display.blit(Text_Game_Over, (0, 147))
            Display.display.blit(Text_Restart, (55, 241))


if __name__ == "__main__":
    pg.init()

    clock = pg.time.Clock()
    game = Game()
    FPS = 60

    while True:
        clock.tick(FPS)
        game.update()
