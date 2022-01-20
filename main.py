import math
import os
import time
import random
import pickle
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
pygame.init()

from car import Car
from vector import Vector

class RaceTrack:
    def __init__(self):
        self.car = Car(20,950,90)
        self.run = True
        self.win = pygame.display.set_mode((1000,1000))
        pygame.display.set_caption("Racing game")
        self.clock = pygame.time.Clock()
        self.PIK = "pickle.dat"
        self.borders = []
        #self.store_borders()
        #self.load_borders()
        self.fill_borders()
        self.last = [None]*len(self.car.laser)

    def fill_borders(self):
        self.borders.append(Vector(0, 900, 0, 999))
        self.borders.append(Vector(0, 900, 600, 800))
        self.borders.append(Vector(600, 800, 700, 700))
        self.borders.append(Vector(700, 700, 550, 600))
        self.borders.append(Vector(550, 600, 250, 600))
        self.borders.append(Vector(250, 600, 150, 500))
        self.borders.append(Vector(150, 500, 150, 100))
        self.borders.append(Vector(150, 100, 350, 50))
        self.borders.append(Vector(350, 50, 700, 400))
        self.borders.append(Vector(700, 400, 1000, 420))
        self.borders.append(Vector(0, 999, 650, 970))
        self.borders.append(Vector(650, 970, 900, 800))
        self.borders.append(Vector(900, 800, 900, 650))
        self.borders.append(Vector(900, 650, 670, 470))
        self.borders.append(Vector(1000, 470, 300, 470))
        self.borders.append(Vector(300, 470, 300, 200))
        self.borders.append(Vector(300, 200, 670, 470))

    def store_borders(self):
        data = self.borders
        with open(self.PIK, "wb") as f:
            pickle.dump(data, f)

    def load_borders(self):
        data = self.borders

        with open(self.PIK, "rb") as f:
            self.borders = pickle.load(f)

    def draw_car(self):
        pygame.draw.circle(self.win,(255,255,123), (self.car.xPos, self.car.yPos),  5)

    def draw_borders(self):
        borderColor = (153, 70, 5)
        for x in self.borders:
            pygame.draw.line(self.win, borderColor, (x.xPos,x.yPos),(x.nX,x.nY),6)

    def input(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.car.angle -= 3
        elif keys[pygame.K_RIGHT]:
            self.car.angle += 3
        if keys[pygame.K_UP]:
            self.car.accelerate(1)
        elif keys[pygame.K_DOWN]:
            self.car.accelerate(-1)

    # Sets end-position of laser to the point of contact with border
    def set_laser_length(self):
        for i,x in enumerate(self.car.laser):
            for y in self.borders:
                v = self.get_collision_point(x,y,True)
                if(v is not None):
                    x.nX = v.xPos
                    x.nY = v.yPos
                    self.last[i] = y

    def output_length(self):
        for x in self.car.laser:
            print(self.distance(self.car.get_x(), self.car.get_y(), x.nX, x.nY))
        print()

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))

    # Returns point if the parameter is true, else returns wether a and b collide
    def get_collision_point(self, a, b, gives_vector):
        x1 = a.xPos
        x2 = a.nX
        y1 = a.yPos
        y2 = a.nY
        x3 = b.xPos
        x4 = b.nX
        y3 = b.yPos
        y4 = b.nY

        try:
            ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
            ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        except:
            ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3))
            ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3))

        if not (gives_vector):
            return ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1
        if ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1:
            intersectionX = x1 + (ua*(x2-x1))
            intersectionY = y1 + (ua*(y2-y1))
            return Vector(intersectionX, intersectionY, 0, 0)
        else:
            return None

    def check_crash(self):
        for x in self.car.laser:
            if (self.distance(self.car.get_x(), self.car.get_y(), x.nX, x.nY)<10):
                self.car = Car(20, 950, 90)

    def loop(self):
        self.win.fill((125,124, 110))
        self.input()
        self.car.update(self.win)
        self.set_laser_length()
        self.check_crash()
        self.output_length()
        self.draw_borders()
        self.draw_car()

        pygame.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    rt = RaceTrack()
   
    while rt.run:
        rt.loop()

    pygame.quit()
    rt.store_borders()
    print('\U0001f697')


# TODO: write a file format to store different racetracks
