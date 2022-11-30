#################################################################
# 15-112: Final Term Project
# name: Arin Pantja
# andrewID: apantja
# Project: Super Paper Mario Lite-112
#################################################################

import random
from math import *
from characters import *
from level import *
from cmu_112_graphics import *

##########################################
# Splash Screen Mode
##########################################

# Referenced 112 Notes from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
def splashScreenMode_redrawAll(app, canvas):
    font = 'MARIOFontv3_2-Solid 26 bold'
    # Draw images!
    canvas.create_image(app.width/2, app.height/2,
    image = ImageTk.PhotoImage(app.splashBgS))
    canvas.create_image(app.width/2,app.height/2, 
    image= ImageTk.PhotoImage(app.titleSplashS))

    # # Draw mario/luigi
    canvas.create_image(app.width/2-200,app.height/2-70, 
    image= ImageTk.PhotoImage(app.splashMarioBgS))
    canvas.create_image(app.width/2+240,app.height/2, 
    image= ImageTk.PhotoImage(app.splashLuigiBg))

    # Instructions on Splash - S for Easy, D for Hard
    canvas.create_text(app.width/2, 440, text='Press D for Easy mode',
                       font=font, fill='white')
    canvas.create_text(app.width/2, 480, text='Press F for Hard mode',
                       font=font, fill='white')
    canvas.create_text(app.width/2, 560, text='Press H for Help',
                       font=font, fill='white')

def splashScreenMode_keyPressed(app, event):
    if (event.key == 'h'):
        app.mode = 'helpMode'
    elif (event.key == 'd'):
            app.mode = 'gameMode'
            app.gameDifficulty = 'Easy'
            # Instantiate Terrain -- pass in iterations
            app.terrainObj = genLevel(11)
            app.terrain = app.terrainObj.generateTerrainArray()
            # Determine how often bullets are spawned
            app.bulletOccurence = 20

    elif (event.key == 'f'):
            app.mode = 'gameMode'
            app.gameDifficulty = 'Hard'
            # Instantiate Terrain -- pass in iterations
            app.terrainObj = genLevel(5)
            app.terrain = app.terrainObj.generateTerrainArray()
            # Determine how often bullets are spawned
            app.bulletOccurence = 10


##########################################
# Game Mode
##########################################

def gameMode_redrawAll(app, canvas):

    ############################################
    # Draw background image
    canvas.create_image(app.width/2,app.height/2, image= ImageTk.PhotoImage(app.starterBg))

    app.terrainObj.drawTerrain(app, canvas)
    drawStats(app, canvas)

    drawBulletBill(app, canvas)
    app.playerMario.redraw(app, canvas)

    ############################################
    # Draw coins
    # newCoin = Coins(app.width/2 + app.scrollX, app.height/2)
    # newCoin.redraw(app, canvas)


def drawStats(app, canvas):
    header = 'MARIOFontv3_2-Solid 24 bold'
    subheader = 'MARIOFontv3_2-Solid 18 bold'
    # Stats - Health, gameMode (easy/hard), Score (points)
    canvas.create_image(100, 40, image= ImageTk.PhotoImage(app.heartImgs))
    ###### HEARTS ######
    heartTextX = 120
    canvas.create_text(heartTextX, 30,
    text= f'{app.playerMario.getHealth()}   ', fill = 'white', font=header)
    canvas.create_text(heartTextX + 20, 35,
    text= '  / 5', fill = 'white', font=header)

    ###### EASY/HARD MODE + PROGRESS TO WIN ######
    # scrollX + 20 everytime
    progress = math.ceil(app.scrollX / (app.winScrollXDist) * 100)
    canvas.create_text(app.width/2, 25,
    text= f'{progress} %', fill = 'white', font=header)

    canvas.create_text(app.width/2, 50,
    text= f'{app.gameDifficulty}', fill = 'white', font=subheader)

    ###### POINTS ######
    canvas.create_image(app.width - 100, 50, image= ImageTk.PhotoImage(app.scoreBarImgS))
    canvas.create_text(app.width - 120, 35,
    text= f'{app.points}', fill = 'white', font=header)


def gameMode_keyPressed(app, event):
    if (event.key == 'h'):
        app.mode = 'helpMode'

# Mario with RESPECT TO THE GAME
    if (event.key == "Left"): 
        # Prevent users from going left during the start of the game (offScreen)
        if app.scrollX > -10:
            app.spriteMode = 'Left'
            app.scrollX -= app.playerMario.getRunSpeed()
            app.playerMario.x -= app.playerMario.getRunSpeed()
            app.spriteCounter = (1 + app.spriteCounter) % len(app.spritesWalkL)

    elif (event.key == "Right"): 
        app.spriteMode = 'Right'
        app.scrollX += app.playerMario.getRunSpeed()
        app.playerMario.x += app.playerMario.getRunSpeed()
        app.spriteCounter = (1 + app.spriteCounter) % len(app.spritesWalkR)

    # Gravity / jump 
    elif (event.key == "Up"): 
        app.spriteMode = 'Up'
        if app.airTime == 0:
            app.jumping = True

    # TEST KEY! Powerup!
    elif (event.key == "Down"): 
        if app.invincibility:
            app.invincibility = False
        else:
            app.invincibility = True


def gravity(app):
    yGravity = 20
    # When mario is not jumping, gravity is turned on
    if app.jumping == False:
        app.playerMario.y += yGravity
   
def gameMode_timerFired(app):

    if app.gameDifficulty == 'Hard':
        app.terrainIterations = 5
    else:
        app.terrainIterations = 9 #9

    # 20 pixels for each of the 30 tiles = 600 x 600 screen
    # Terrain colision check -- turn on gravity
    if app.playerMario.collisionHit(app.terrain) == False:
        gravity(app)

    playerJump(app)

    # Add bulletBill to a list, every x frequency
    # Create bullet objects, add them to a list
    app.bulletFreq += 1
    
    if app.dmgTimerRun == True:
        app.damageFeedbackTimePassed += 1

    spawnBulletBill(app)

    app.spriteCounterCoin = (1 + app.spriteCounterCoin) % len(app.spritePhotoImages)

    loseGame(app)
    winGame(app)

def resetDmgCounter(app):
    app.damageFeedbackTimePassed = 0

# Periodically spawn bulletBills onto the screen, tracking mario Y position
def spawnBulletBill(app):
    if (app.bulletFreq % app.bulletOccurence == 0):
        marioYRange = int(app.playerMario.y // 20)
        newBullet = bulletBill(app.width + app.scrollX, 
        random.randint(marioYRange - 1,marioYRange + 1) * 20, app.bulletDamage)
        app.bulletBillList.append(newBullet)

    # Increase cx of projectiles
    for bullet in app.bulletBillList:
        bullet.x -= 15 
        if boundsIntersect(app, app.playerMario.getBounds(), bullet.getBounds()):
            if app.invincibility == False:
                app.playerMario.health -= 1

            app.bulletBillList.remove(bullet)
            app.damageFeedback = True
            app.dmgTimerRun = True
            if app.damageFeedbackTimePassed >= 3:
                print("Remove explosion feedback")
                resetDmgCounter(app)               
                app.damageFeedback = False
                app.dmgTimerRun = False
        # OOO check
        if bullet.x < 0:
            app.bulletBillList.remove(bullet)

# Check if there are intersecting boundaries between two objects
def boundsIntersect(app, boundsA, boundsB):
    (ax0, ay0, ax1, ay1) = boundsA
    (bx0, by0, bx1, by1) = boundsB
    return ((ax1 >= bx0) and (bx1 >= ax0) and
            (ay1 >= by0) and (by1 >= ay0))

# Jump with Gravity
def playerJump(app):

    if app.jumping == True:
        # How long mario is in the air
        app.airTime += 1
        app.jumpTime += 1
        app.dy += 1.2
        app.playerMario.y -= 7 * app.dy

    if app.jumpTime == 5:
            app.airTime += 1
            app.dy = 0
            app.jumping = False
            app.jumpTime = 0

    # Own timer to disallow players to jump while airbone 
    if app.airTime == 6:
            app.airTime = 0


def loseGame(app):
    if math.floor(app.playerMario.y / 20) >= app.cols or app.playerMario.health <= 0:
        app.mode = 'gameOverMode'

        
def winGame(app):
    # '480 pixels' per game - 15 pixels per scrollX (movement)
    # movement * pixels in game
    if app.scrollX >= app.winScrollXDist:
        app.mode = 'gameWinMode'


def drawBulletBill(app, canvas):
    # Loop through all bullet bills, and draw them on the canvas
    for bullets in app.bulletBillList:
        bullets.redraw(app, canvas)

##########################################
# Help Mode
##########################################

def helpMode_redrawAll(app, canvas):
    header = 'MARIOFontv3_2-Solid 36 bold'
    font = 'MARIOFontv3_2-Solid 22 bold'

    canvas.create_image(app.width/2,app.height/2, 
    image= ImageTk.PhotoImage(app.sideSplashBgS))

    canvas.create_text(app.width/2, 150, text='Help Screen', 
                       font=header, fill='white')
    canvas.create_text(app.width/2, 210, text='How to Play',
                       font=font, fill='white')
    canvas.create_text(app.width/2, 240, text='Arrow keys to move, jump',
                       font=font, fill='white')
    canvas.create_text(app.width/2, 270, text='Avoid BulletBill and projectiles!',
                       font=font, fill='white')  
    canvas.create_text(app.width/2, 300, text='Collect coins and save Luigi!',
                       font=font, fill='white')                
    canvas.create_text(app.width/2, 500, text='Press B to return to the main menu',
                       font=font, fill='white')

def helpMode_keyPressed(app, event):
    if (event.key == 'b'):
        app.mode = 'splashScreenMode'
        resetGame(app)

##########################################
# GameOver Mode
##########################################

def gameOverMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2,app.height/2, 
    image= ImageTk.PhotoImage(app.sideSplashBgS))
    font = 'MARIOFontv3_2-Solid 26 bold'
    subtitle = 'MARIOFontv3_2-Solid 22 bold'

    canvas.create_text(app.width/2, 150, text='Game Over!', 
                       font=font, fill='white')
    canvas.create_text(app.width/2, 190, text="You didn't manage to save Luigi in time..",
                       font=subtitle, fill='white')
    canvas.create_text(app.width/2, 360, text='Press R to try again!',
                       font=subtitle, fill='white')
    canvas.create_text(app.width/2, 400, text='Press B to go back',
                       font=subtitle, fill='white')

    # canvas.create_text(app.width/2, 350, text=f' You earnt {app.points} points',
    #                    font=font, fill='white')

def gameOverMode_keyPressed(app, event):
    if (event.key == 'h'):
        app.mode = 'helpMode'
        
    elif (event.key == 'r'):
        app.mode = 'gameMode'
        resetGame(app)
    elif (event.key == 'b'):
        app.mode = 'splashScreenMode'
        resetGame(app)

# Reset all in-game variables
def resetGame(app):
    appStarted(app)

##########################################
# GameWin Mode
##########################################

def gameWinMode_redrawAll(app, canvas):
    font = 'MARIOFontv3_2-Solid 40 bold'
    subheader = 'MARIOFontv3_2-Solid 26 bold'


    canvas.create_image(app.width/2,app.height/2, 
    image= ImageTk.PhotoImage(app.sideSplashBgS))

    canvas.create_text(app.width/2,300, text='You saved Luigi!', 
                       font=font, fill='white')
    canvas.create_text(app.width/2, 350, text='B to go back',
                       font=subheader, fill='white')
    # canvas.create_text(app.width/2, 350, text=f' You earnt {app.points} points',
    #                    font=font, fill='black')

def gameWinMode_keyPressed(app, event):

    if (event.key == 'b'):
            app.mode = 'splashScreenMode'
            resetGame(app)

##########################################
# Main App
##########################################

def createImg(app, source, scale):
    loadImg = app.loadImage(source)
    return app.scaleImage(loadImg, scale)

def appStarted(app): 
    app.mode = 'splashScreenMode'
    app.messages = ['appStarted']
    app.gameDifficulty = 'Easy'
    app.winScrollXDist = 20 * 100 # 20 pixels for each movement

    app.scrollX = 0
    app.cols = 30
    app.rows = 30
    app.margin = 5

    # Stats for the game
    app.points = 0
    app.spritePhotoImages = loadAnimatedGif('images/coin.gif')
    app.spriteCounterCoin = 0

    # 30 x 30 grid of 20 for main game screen
    app.screenTiles = [ ([''] * app.cols) for i in range(app.rows)]

    ##########################################
    # Images from https://www.mariowiki.com/Gallery:Super_Paper_Mario 
    app.starterBg = createImg(app, 'images/gameBg.jpg', 1)
    app.splashBgS = createImg(app, 'images/splash/splashBg.jpg', 4/5)

    app.titleSplashS = createImg(app, 'images/splash/titleSplash.png', 1/3)
    app.sideSplashBgS = createImg(app, 'images/splash/sideSplash.png', 9/10)

    app.splashMarioBgS = createImg(app, 'images/splash/marioSplash.png', 2/3)
    app.splashLuigiBg = createImg(app, 'images/splash/luigiSplash.png', 1/2)

    app.bulletBillImgS = createImg(app, 'images/characters/bulletBill.png', 2/5)
    app.invincibilityPowerUp = createImg(app, 'images/characters/invincibilityPowerUp.png', 1/15)

    # Images from https://www.spriters-resource.com/wii/superpapermario/ 
    app.heartImgs = createImg(app, 'images/heart.png', 2/13)
    app.coinBarImgS = createImg(app, 'images/coinBar.png', 1/11)
    app.scoreBarImgS = createImg(app, 'images/scoreBar.png', 1)
    app.doorWin = createImg(app, 'images/door.png', 1/4)

    app.damageFeedbackImgS = createImg(app, 'images/damage.png', 1/8)


    # With reference from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
    # Sprite images - 1440 x 360 - 480 / still  
    # Scaled down sprite images -- 576 x 144 - 192
    spriteWalkR = createImg(app, 'images/characters/marioWalkR.png', 2/5)
    spriteWalkL = createImg(app, 'images/characters/marioWalkL.png', 2/5)
    app.spriteJumpL = createImg(app, 'images/characters/marioJumpL.png', 1/5)
    app.spriteJumpR = createImg(app, 'images/characters/marioJumpR.png', 1/5)

    app.spritesWalkR = [ ]
    app.spritesWalkL = [ ]
    for i in range(3):
        spriteR = spriteWalkR.crop((10+192*i, 10, 182+192*i, 144))
        spriteL = spriteWalkL.crop((10+192*i, 10, 182+192*i, 144))

        app.spritesWalkR.append(spriteR)
        app.spritesWalkL.append(spriteL)
        app.spriteCounter = 0

    # Instantiate Mario ##########################################
    x, y, health, height, width = app.width/2, app.height/2, 5, 40, 20
    app.playerMario = Mario(x, y, health, height, width)

    app.jumping = False
    app.spriteJumping = False
    app.jumpTime = 0
    app.airTime = 0
    app.dy = 0
    app.spriteMode = 'right'
    app.invincibility = False

    # Instantiate bulletBills ##########################################
    app.bulletFreq = 0
    app.bulletBillList = []
    app.bulletDamage = 2
    app.damageFeedback = False
    app.damageFeedbackTimePassed = 0
    app.dmgTimerRun = False

    # Instantiate coins 
    app.coinsList = []
    app.coinPoints = 5

# With reference to 112 Website - https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#animatedGifs
def loadAnimatedGif(path):
    # load first sprite outside of try/except to raise file-related exceptions
    spritePhotoImages = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            spritePhotoImages.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e:
            return spritePhotoImages

def appStopped(app):
    app.messages.append('appStopped')
    print('appStopped!')

runApp(width=600, height=600)
