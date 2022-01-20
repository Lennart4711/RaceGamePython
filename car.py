from vector import Vector
import math
import pygame

class Car:
    def __init__(self, x, y, r):
        self.xPos = x
        self.yPos = y
        self.angle = r
        self.speed = 0
        self.vX = 0
        self.vY = 0
        self.laser = [Vector(0,0,0,0)]*5
        self.hitbox = Vector(self.xPos-5, self.yPos, self.xPos+5, self.yPos)
        self.accFactor = 0.3
        self.driven_distance = 0

    def get_x(self):
        return self.xPos

    def get_y(self):
        return self.yPos

    # Sets a hitbox at the position of the car
    def set_hitbox(self):
        radians = (2*30+self.angle+180+30) * math.pi/180
        x = self.xPos + 20 * math.cos(radians)
        y = self.yPos + 20 * math.sin(radians)
        self.hitbox = Vector(self.xPos, self.yPos, x, y)

    # Sets the direction for every laser relative to the car's rotation
    def set_lasers(self):
        for i in range(len(self.laser)):
            turn = 360/len(self.laser)
            turn = 30
            radians = (270+ self.angle+i*turn - turn/2*(len(self.laser)-1)) * math.pi /180
            x = self.xPos + 600 * math.cos(radians)
            y = self.yPos + 600 * math.sin(radians)
            self.laser[i] = Vector(self.xPos,self.yPos,x,y)

    def draw_laser(self, win):
        laserColor = (255,54,45)
        for x in self.laser:
            pygame.draw.line(win, laserColor,(x.nX,x.nY), (self.xPos,self.yPos))

        x = self.laser[len(self.laser) // 2]
        pygame.draw.line(win, (12,12,123),(x.nX,x.nY), (self.xPos,self.yPos))

    def accelerate(self,b):
        xN = math.sin(2 * math.pi * (self.angle / 360))
        yN = math.cos(2 * math.pi * (self.angle / 360))
        # Adds to velocity vector, using minus for y because pygame uses 0,0 as top-left corner
        self.vX += xN * self.accFactor*b
        self.vY -= yN * self.accFactor*b

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))

    def update(self, win):
        self.draw_laser(win)
        self.accelerate(1)
        self.set_hitbox()
        self.set_lasers()

        self.driven_distance += self.distance(self.xPos, self.yPos,self.xPos+self.vX, self.yPos+self.vY)/10

        #print(self.driven_distance)
        self.xPos += self.vX
        self.yPos += self.vY
        self.vX -= self.vX * 0.06
        self.vY -= self.vY * 0.06

        if(self.xPos<0):
            self.xPos += 1000
        elif(self.xPos>1000):
            self.xPos -= 1000
        if(self.yPos<0):
            self.yPos += 1000
        elif(self.yPos>1000):
            self.yPos -= 1000
