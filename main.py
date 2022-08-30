from calendar import c
import math
import os
import time
from neural_network import NeuralNetwork

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.init()

from car import Car
from vector import Vector
from save import fill_borders, get_checks, read_borders


class RaceTrack:
    def __init__(self):
        self.shape = [7, 5, 4, 2]
        self.amount = 10
        self.run = True
        self.win = pygame.display.set_mode((600,600))
        pygame.display.set_caption("Racing game")
        self.clock = pygame.time.Clock()
        self.borders = []
        self.checks = []
        #fill_borders(self.borders)
        read_borders('borders.txt', self.borders)
        get_checks(self.checks)
        self.cars = [Car(200+x, 60+x, 90,self.checks, NeuralNetwork(self.shape)) for x in range(self.amount)]

        self.bestscore = 0
        self.best_nn = None
        self.last = 0


    def draw_cars(self):
        for car in self.cars:
            pygame.draw.circle(self.win,(255,255,123), (car.xPos, car.yPos),  2)

    def draw_borders(self):
        borderColor = (153, 70, 5)
        for x in self.borders:
            pygame.draw.line(self.win, borderColor, (x.xPos,x.yPos),(x.nX,x.nY),2)
        for el in self.checks:
            pygame.draw.circle(self.win,(155,10,12), el,  3)

    def input(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.run = False
            if(event.type == pygame.MOUSEBUTTONDOWN):
                if event.button == 1:
                    self.amount += 1
                    #self.checkps.append(pygame.mouse.get_pos())
                if event.button == 3:
                    del self.checkps[-1]

        # keys = pygame.key.get_pressed()

        # if keys[pygame.K_LEFT]:
        #     self.cars[0].turn(-1) 
        # elif keys[pygame.K_RIGHT]:
        #     self.cars[0].turn(+1) 
        # if keys[pygame.K_UP]:
        #     self.cars[0].accelerate(1)
        # elif keys[pygame.K_DOWN]:
        #     self.cars[0].accelerate(-1)

    # Sets end-position of laser to the point of contact with border
    def set_laser_length(self, car):
        for i,x in enumerate(car.lasers):
            for y in self.borders:
                v = self.get_collision_point(x,y,True)
                if(v is not None):
                    x.nX = v.xPos
                    x.nY = v.yPos
            d = self.distance(car.get_x(), car.get_y(), x.nX, x.nY)
            car.lengths[i] = min(d, 200)
                

    def output_length(self):
        for x in self.car.lasers:
            print(self.distance(self.car.get_x(), self.car.get_y(), x.nX, x.nY))
        print()

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))

    # Returns point if the parameter is true, else returns wether a and b collide
    def get_collision_point(self, a, b, gives_vector):
        if self.distance(a.xPos, a.yPos, b.xPos, b.yPos)>= 400:
            return None
        
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
    

    def check_crash(self, car):
        for laser in car.lasers:
            if (self.distance(car.get_x(), car.get_y(), laser.nX, laser.nY)<3):
                car.alive = False

    def check_restart(self):
        restart = not any(car.alive for car in self.cars) or (time.time()-self.last) >= 60
        if restart:
            self.last = time.time()
            self.cars = self.new_generation()

    def new_generation(self):
        bestcar = self.cars[0]
        for car in self.cars:
            if car.score >= bestcar.score:
                bestcar = car
        
        if bestcar.score >= self.bestscore:
            self.bestscore = bestcar.score
            best_nn = bestcar.nn.get_deep_copy()
            self.best_nn = best_nn
        else:
            best_nn = self.best_nn

        new = [Car(200+x, 60+x, 90,self.checks, bestcar.nn.reproduce(.15)) for x in range(self.amount)]
        new[0] = Car(new[0].xPos, new[1].yPos, 90, self.checks, self.best_nn)
        return new

    def loop(self):
        self.win.fill((125,124, 110))
        self.input()
        for car in self.cars:
            if car.alive:
                car.update(self.win)
                self.set_laser_length(car)
                car.move()
                self.check_crash(car)
            if len(car.checks)<= 0:
                car.checks = self.checks

        self.clock.tick(60)
        self.draw_borders()
        self.draw_cars()
        self.check_restart()
        pygame.display.update()
            


if __name__ == "__main__":
    rt = RaceTrack()
   
    while rt.run:
        rt.loop()

    pygame.quit()
    # with open("checks.txt", 'w') as s:
    #     s.write(str(rt.checkps))
    print('\U0001f697')


