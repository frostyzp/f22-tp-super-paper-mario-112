from cmu_112_graphics import *
import random
import math

##########################################
# All characters inherit from Characters class
##########################################

class Character(object):
    def __init__(self,x, y, health):
        self.x = x
        self.y = y
        self.health = health

    def getCx(self):
        return int(self.cx)
        
    def getCy(self):
        return int(self.cy)

    def getHealth(self):
        return self.health

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height

    def getRunSpeed(self):
        return 20 #20 px 

    def getHealth(self):
        return self.health

    # Checks within 2d list if there is collision
    # Returns False if there is no collision
    def collisionHit(self, array):
        if array[math.floor(self.y / 20)][math.floor(self.x / 20)] != '':
            return False
        return True

    # returns absolute bounds, not taking scrollX into account
    def getBounds(self):
        (x0, y1) = (self.x, abs(self.height - self.y))
        (x1, y0) = (self.x + self.width, y1 - self.height)
        return (x0, y0, x1, y1)

##########################################
# Playable Character
##########################################

class Mario(Character):
    def __init__(self, x, y, health, height, width):
        super().__init__(x, y, health)
        self.height = height
        self.width = width

##########################################
# Ad-hoc -- Coins / Bullet Bill
##########################################

class Coins(object):
    height = 20

    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def earnPoint(self):
        return 5

class bulletBill(Character):
    bulletSpeed = 15

    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage
        self.height = 20 
        self.width = 40

    def redraw(self, app, canvas):
        # canvas.create_oval(self.x, self.y,
        #                    self.x+20, self.y+20,
        #                    fill='white', outline='red', width=1)
        canvas.create_image(self.x, self.y, 
        image = ImageTk.PhotoImage(app.bulletBillImgS))



