import pygame as pg
from pygame import Vector2 as v
from pygame.locals import *
from random import choice as c, randint as r
from sys import exit

pg.init()


class Display:
    def __init__(self):
        self.dimension = v(300, 600)
        self.display = pg.display.set_mode(self.dimension)
        self.title = pg.display.set_caption("Frog Test")


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

            if key[K_DOWN] and self.position.y < DISPLAY.dimension.y - self.dimension.x:
                self.position.y += self.velocity.y

            if key[K_LEFT] and self.position.x > 0:
                self.position.x -= self.velocity.x

            if key[K_RIGHT] and self.position.x < DISPLAY.dimension.x - self.dimension.x:
                self.position.x += self.velocity.x

    def died(self):
        self.position = v(140, 540)
        self.lifes -= 1

    def scored(self) -> bool:
        if frog.position.y < 0:
            frog.position.y = 580
            frog.score += 1
            return True
        else:
            return False

    def reset(self):
        self.position = v(140, 540)
        self.dimension = v(20, 20)
        self.lifes = 3
        self.score = 0


class Car:
    def __init__(self, x, y, X, vel, direction):
        self.position = v(x, y)
        self.dimension = v(X, frog.dimension.y)
        self.velocity = v(vel, 0)
        self.color = (200, 10, 10)
        self.direction = direction

    def move(self, aggregator):
        if self.direction:
            self.position.x -= self.velocity.x * aggregator
            if self.position.x < -self.dimension.x:
                self.position.x = DISPLAY.dimension.x
        else:
            self.position.x += self.velocity.x * aggregator
            if self.position.x > DISPLAY.dimension.x:
                self.position.x = -self.dimension.x


class Game:
    def __init__(self):
        self._aggregator = 1
        self._cars = list()
        self._cached = list()
        self._paused = False
        self._create_roads()

    def update(self):
        DISPLAY.display.fill((0, 0, 0))
        self._show_score()
        carsHitbox = [pg.draw.rect(DISPLAY.display, car.color,
                                   (car.position, car.dimension)) for car in self._cars]
        frogHitbox = pg.draw.rect(DISPLAY.display, frog.color,
                                  (frog.position, frog.dimension))

        for car in self._cars:
            car.move(self._aggregator)

        if frog.scored():
            self._create_roads()
            self._aggregator = self._aggregator + \
                0.1 if self._aggregator < 2 else self._aggregator

        for carHitbox in carsHitbox:
            if frogHitbox.colliderect(carHitbox):
                frog.died()

        self._aggregator = 5 if frog.lifes == 0 else self._aggregator

    def reset(self):
        self._create_roads()
        frog.reset()
        self._aggregator = 1

    def pause(self):
        if not self._paused:
            for car in self._cars:
                self._cached.append(car.velocity)
                car.velocity = v(0, 0)
            frog.velocity = v(0, 0)
            self._paused = True
        else:
            for i, car in enumerate(self._cars):
                car.velocity = self._cached[i]
            frog.velocity = v(frog.dimension.x, frog.dimension.y)
            self._paused = False
            self._cached.clear()

    def _create_roads(self):
        self._cars.clear()
        for i, h in enumerate((120, 200, 280, 360, 440)):
            q = r(2, 3)
            a = r(12, 30)/10
            x = r(50, 90) if q == 2 else r(40, 60)
            d = c([True, False])
            g = r(x+int(x/3), DISPLAY.dimension.x - x * q)
            for i in range(q):
                self._cars.append(Car(i*g, h, x, a, d))

    @staticmethod
    def _show_score():
        FONT = pg.font.get_default_font()
        WHITE = (255, 255, 255)

        SysFont = pg.font.SysFont(FONT, 30).render
        Text_Player_Lifes = SysFont(f"lifes: {frog.lifes}", True, WHITE)
        Text_Player_Points = SysFont(f"score: {frog.score}", True, WHITE)

        DISPLAY.display.blit(Text_Player_Lifes, (200, 5))
        DISPLAY.display.blit(Text_Player_Points, (200, 28))

        if frog.lifes == 0:
            Text_Game_Over = pg.font.SysFont(FONT, 70).render(
                "GAME OVER", True, WHITE)

            Text_Restart = SysFont(
                "Press 'r' for restart", True, WHITE)

            DISPLAY.display.blit(Text_Game_Over, (0, 147))
            DISPLAY.display.blit(Text_Restart, (55, 241))


if __name__ == "__main__":
    clock = pg.time.Clock()
    DISPLAY = Display()
    frog = Frog()
    game = Game()
    FPS = 60

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                key = pg.key.get_pressed()
                frog.move()

                if key[K_r]:
                    game.reset()

                if key[K_SPACE]:
                    game.pause()

        clock.tick(FPS)
        game.update()
        pg.display.update()
