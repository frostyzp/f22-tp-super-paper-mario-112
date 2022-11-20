from cmu_112_graphics import *
import random

##########################################
# All characters inherit from Characters class
##########################################

class Character(object):
    def __init__(self,cx, cy, health):
        self.cx = cx
        self.cy = cy
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
        return self.width

    def getRunSpeed(self):
        return 20 #20 px 

    def getHealth(self):
        return self.health

##########################################
# Playable Character
##########################################

class Mario(Character):
    def __init__(self, cx, cy, health, height, width):
        super().__init__(cx, cy, health)
        self.height = height
        self.width = width

##########################################
# Enemies
##########################################

class Enemy(Character):
    def __init__(self, cx, cy, health, height, width):
        super().__init__(cx, cy, health)
        self.health = health
        self.height = height
        self.width = width

    def shootProjectiles(self):
        # shoot periodically, under Timerfired
        #

        pass

##########################################
# Ad-hoc -- Coins / Bullet Bill
##########################################

class Coins(object):
    height = 20
    coinList = []

    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def addCoin(self, coin):
        # append coin object to a list, which will be rendered
        self.coinList.append(coin)

    def removeCoin(self, coin):
        self.coinList.pop(coin)

    def earnPoint(self):
        return 5


class bulletBill(object):

    def __init__(self, damage):
        self.damage = damage
        self.bullets = []

    def addBullet(self, y, appWidth):
        self.bullets.append(appWidth, y)

    def damage(self):
        return self.damage


