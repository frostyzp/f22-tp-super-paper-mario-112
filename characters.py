from cmu_112_graphics import *
import random
import math

##########################################
# Characters
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

    # Checks within 2d list of terrain if there is collision
    # Returns False if there is no collision
    def collisionHit(self, array):
        checkGround = array[math.floor(self.y // 20)][math.floor(self.x // 20)]

        if checkGround != 'ground': 
            return False
        # if checkGround2 != 'ground':
            # return False

        return True

    def sideCollision(self, array):
        checkGround2 = array[math.floor((self.y - 20) // 20)][math.floor((self.x + 20) // 20)]
        
        if self.collisionHit(array) == True and checkGround2 != 'ground':
            return False
        return True

    # returns absolute bounds, not taking scrollX into account
    def getBounds(self):
        (x0, y1) = (self.x, self.y)
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

    def redraw(self, app, canvas):
        (x0, y0, x1, y1) = self.getBounds()
        spriteR = app.spritesWalkR[app.spriteCounter]
        spriteL = app.spritesWalkL[app.spriteCounter]
    
        # Drawing appropiate sprite images
        if app.spriteInAir == False and app.spriteMode == 'Right':
            canvas.create_image(x0 - app.scrollX, y0 + 5, image=ImageTk.PhotoImage(spriteR))
        elif app.spriteInAir == False and app.spriteMode == 'Left':
            canvas.create_image(x0 - app.scrollX, y0 + 5, image=ImageTk.PhotoImage(spriteL))
        elif app.spriteInAir == True and app.spriteMode == 'Left':
            canvas.create_image(x0 - app.scrollX, y0 + 5, image=ImageTk.PhotoImage(app.spriteJumpL))
        elif app.spriteInAir == True and app.spriteMode == 'Right':
            canvas.create_image(x0 - app.scrollX, y0 + 5, image=ImageTk.PhotoImage(app.spriteJumpR))

            
        # Drawing damage feedback from enemeies/projectiles
        if app.damageFeedback:
            coordX = self.x
            coordY = self.y - 20
            canvas.create_image(coordX - app.scrollX, coordY, 
        image = ImageTk.PhotoImage(app.damageFeedbackImgS))

        # Drawing invincibility, if obtained in the level
        if app.invincibility:
            canvas.create_image(x0 - app.scrollX - 20, y0 + 5, image=ImageTk.PhotoImage(app.invincibilityPowerUp))
            canvas.create_text(x0 - app.scrollX - 20, y0 - self.height - 20, text='Invincible!',
            font='MARIOFontv3_2-Solid 10 bold', fill='white')

##########################################
# Ad-hoc -- Bullet Bill / Coins
##########################################

class bulletBill(Character):
    bulletSpeed = 15

    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage
        self.height = 20 
        self.width = 40

    def redraw(self, app, canvas):
        canvas.create_image(self.x - app.scrollX, self.y, 
        image = ImageTk.PhotoImage(app.bulletBillImgS))

        
class Coins(object):
    height = 20

    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def redraw(self, app, canvas):
        pass
        photoImage = app.spritePhotoImages[app.spriteCounterCoin]
        canvas.create_image(200, 200, image=photoImage)
        

