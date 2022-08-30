from vector import Vector
import math
import pygame
from neural_network import NeuralNetwork
import time

class Car:
    def __init__(self, x, y, r, checks, nn=None):
        self.xPos = x
        self.yPos = y
        self.angle = r
        self.vX = 0
        self.vY = 0
        self.checks = checks
        self.lasers = [Vector(0,0,0,0)]*6
        self.accFactor = 0.15
        self.nn = nn
        self.nn = self.nn.reproduce(.3)
        # self.nn.set_random_weights()
        self.score = 0
        self.alive = True
        self.speed = 0
        self.lengths = [0]*len(self.lasers)
        self.driven_dist = 0
        self.last = time.time()

    def get_x(self):
        return self.xPos

    def get_y(self):
        return self.yPos

    # Sets the direction for every laser relative to the car's rotation
    def set_lasers(self):
        for i in range(len(self.lasers)):
            turn = 360/len(self.lasers)
            turn = 20
            radians = (270+ self.angle+i*turn - turn/2*(len(self.lasers)-1)) * math.pi /180
            x = self.xPos + 600 * math.cos(radians)
            y = self.yPos + 600 * math.sin(radians)
            self.lasers[i] = Vector(self.xPos,self.yPos,x,y)

    def draw_laser(self, win):
        laserColor = (155,20,155)
        for x in self.lasers:
            pygame.draw.line(win, laserColor,(x.nX,x.nY), (self.xPos,self.yPos))

    def accelerate(self,b):
        xN = math.sin(2 * math.pi * (self.angle / 360))
        yN = math.cos(2 * math.pi * (self.angle / 360))
        # Adds to velocity vector, using minus for y because pygame uses 0,0 as top-left corner
        self.vX += xN * self.accFactor*b
        self.vY -= yN * self.accFactor*b

    def turn(self, direction=1):
        #direction = 1 or -1
        self.angle += 2 * direction
        if self.angle > 360: self.angle -= 360
        if self.angle < 0: self.angle += 360

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))

    def update(self, win):
        if not self.alive:
            return
        
        self.draw_laser(win) 
        self.accelerate(.1)
        self.set_lasers()
        
        self.xPos += self.vX
        self.yPos += self.vY
        self.vX -= self.vX * 0.06
        self.vY -= self.vY * 0.06
        #self.driven_dist += self.distance(self.xPos, self.yPos,self.xPos+self.vX, self.yPos+self.vY)/10
        

        new = [check for check in self.checks if self.distance(self.xPos, self.yPos, check[0], check[1]) > 20]
        t = self.score
        self.score += len(self.checks) - len(new)
        if self.score != t:
            self.last = time.time()
        self.checks = new

        if 0 > self.xPos > 600 or 0 > self.yPos > 600:
            self.alive = False

        if time.time() - self.last >= 20:
            self.alive = False

    def move(self):
        out = self.nn.forward(self.lengths+[self.speed])
        self.turn((out[0]-.5)*2)
        self.accelerate(out[1])