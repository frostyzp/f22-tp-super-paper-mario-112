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
        return self.cx
        
    def getCy(self):
        return self.cy

    def getHealth(self):
        return self.health

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.width

    def getRunSpeed(self):
        return 10

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

    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def earnPoint(self):
        return 5


class bulletBill(object):

    def __init__(self, damage):
        self.damage = damage
        self.bullets = []

    def addBullet(self, y, appWidth):
        self.bullets.append(appWidth, y)

    def damage(self):
        return -self.damage





        ##Character Physics
    if (app.TubeHere == False) and (app.PlatformHere == False) and (app.GapHere == False) and (app.HillHere == False) and (app.WinBlockHere == False):
        Character.gravity(app)
    
    if app.GapHere == True:
        app.isJumping = False

    #All Jumping Functions
    if app.isJumping == True:
        app.restrictJump = True
    else:
        app.restrictJump = False
    if app.isJumping == True:
        Character.upwardsVelocity(app)
        app.jumpDelay += 1
        if app.jumpDelay == 10:
            app.isJumping = False
            app.isFalling = True
            app.jumpDelay = 0
            app.upVelocityDecrease = 60
   
    if app.isFalling == True:
        app.fallingDelay += 1
    if app.fallingDelay > 8:
        app.isFalling = False
        app.fallingDelay = 0