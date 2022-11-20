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
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 250, text='Press any key for the game!',
                       font=font, fill='black')

    # Draw images!
    canvas.create_image(app.width/2, app.height/2,
    image = ImageTk.PhotoImage(app.splashBgS))
    canvas.create_image(app.width/2,app.height/2, 
    image= ImageTk.PhotoImage(app.titleSplashS))
    # # Draw mario/luigi
    canvas.create_image(app.width/2-200,app.height/2+100, 
    image= ImageTk.PhotoImage(app.splashMarioBgS))
    canvas.create_image(app.width/2+200,app.height/2, 
    image= ImageTk.PhotoImage(app.splashLuigiBg))

    # Instructions on Splash - S for Easy, D for Hard


def splashScreenMode_keyPressed(app, event):

    if (event.key == 'h'):
        app.mode = 'helpMode'
    elif (event.key == 's'):
            app.mode = 'gameMode'


##########################################
# Game Mode
##########################################

def gameMode_redrawAll(app, canvas):

    ############################################
    # Draw background image
    canvas.create_image(app.width/2,app.height/2, image= ImageTk.PhotoImage(app.starterBg))

    drawMario(app, canvas)
    drawTerrain(app, canvas)
    drawStats(app, canvas)

    # Draw random platforms here
    # for (cx, cy) in app.platforms:

def drawMario(app, canvas):
    # Draw sprite image of mario here
    # runningLeft, runningRight, jumping,
    # x1, y1 (top left), x2, y2 (bottom left)
    canvas.create_oval(app.marioCx-app.marioW, app.marioCy-app.marioH, 
    app.marioCx+app.marioW, app.marioCy+app.marioH, fill='cyan')

def drawTerrain(app, canvas):
    # Draw the terrain, which moves along scrollX and scrollY

    # Max height, width
    for (tX, tY, tLength) in app.terrain:
        tX -= app.scrollX  
        # tLength -= app.scrollX
        # tY += app.scrollY
        # Draw image here
        canvas.create_rectangle(tX, tY, tX + tLength, app.height, 
        fill='lightGreen')


def gravity(app):
    yGravity = 15
    app.marioCy += yGravity


def drawStats(app, canvas):
    canvas.create_text(50, 20,
    text= f'{app.playerMario.getHealth()}', fill = 'yellow', font=f'Arial {20} bold')
    canvas.create_text(app.width/2, 20,
    text= f'{app.gameMode}', fill = 'yellow', font=f'Arial {20} bold')

def gameMode_keyPressed(app, event):
    
    if (event.key == 'h'):
        app.mode = 'helpMode'
    if (event.key == "Left"): 
        # Start screen (left) constraint
        if app.scrollX > -10:
            app.scrollX -= app.playerMario.getRunSpeed()
    elif (event.key == "Right"): 
        app.scrollX += app.playerMario.getRunSpeed()
    elif (event.key == "Up"): 
        print("JUMP!")
        # Gravity / jump
        app.jumping = True

def groudCollision(app, tX, tY):
    print('mariocy', app.marioCy)
    # Check to see if there are any collisions with the ground
    # Gravity is applied when there is no collision detected
    tX += app.scrollY
    # tY -= app.scrollX

    ###### HOW TO MAKE SURE THAT WHEN CHECKING Y COORDINATE,
    # WE ARE ONLY LOOKING AT THAT EXACT X
    if app.marioCy > tY: #and app.marioCx + app.marioW > cx:
        return True
    elif app.marioCx > tX:
        return True
    return False


def gameMode_timerFired(app):
    app.jumpHeight = 5
    # Ground collision detection
    for (tX, tY, tLength) in app.terrain:
        # update X coordinate
        if groudCollision(app, tX, tY) == False:
            gravity(app)
            print('gravity on')
        print('Terrain Cx, Cy!', tX, tY)

    app.jumpHeight = 10
    app.velocityJump = app.jumpHeight
 
    # Jump with Gravity
    if app.jumping == True:
        app.jumpTime += 1
        app.marioCy -= 12
    if app.jumpTime > 8:
        if groudCollision(app, tX, tY) == False:
            app.marioCy += 12
            app.jumping = False
            app.jumpTime = 0


def drawBulletBill(app, canvas):
    # app.bulletBill

    pass

##########################################
# Help Mode
##########################################

def helpMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 150, text='This is the help screen!', 
                       font=font, fill='black')
    canvas.create_text(app.width/2, 250, text='(Insert helpful message here)',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 350, text='Press any key to return to the game!',
                       font=font, fill='black')

def helpMode_keyPressed(app, event):
    app.mode = 'gameMode'

##########################################
# GameOver Mode
##########################################

def gameOverMode_redrawAll (app, canvas):
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 150, text='Help Screen', 
                       font=font, fill='black')
    canvas.create_text(app.width/2, 250, text='Left, right, and up arrow keys to move',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 350, text='Press any key to return to the game!',
                       font=font, fill='black')

def gameOverMode_keyPressed(app, event):
    app.mode = 'gameMode'

##########################################
# Main App
##########################################

def appStarted(app): 
    app.mode = 'splashScreenMode'
    app.messages = ['appStarted']
    app.gameMode = 'Easy'

    app.scrollX = 0
    app.scrollY = 0

    app.cols = 60
    app.rows = 60

    app.board = [ ([''] * app.cols) for i in range(app.rows)]

    ##########################################
    # Images from https://www.mariowiki.com/Gallery:Super_Paper_Mario 
    app.starterBg = app.loadImage('images/gameBg.jpg')
    app.splashBg = app.loadImage('images/splash/splashBg.png')
    app.splashBgS = app.scaleImage(app.splashBg, 4/5)
    app.titleSplash = app.loadImage('images/splash/titleSplash.png')
    app.titleSplashS = app.scaleImage(app.titleSplash, 1/3)

    app.splashMarioBg = app.loadImage('images/splash/marioSplash.png')
    app.splashMarioBgS = app.scaleImage(app.splashMarioBg, 2/3)
    app.splashLuigiBg = app.loadImage('images/splash/luigiSplash.png')
    app.splashLuigiBgS = app.scaleImage(app.splashLuigiBg, 1/10)

    # Instantiate Terrain ##########################################
    app.terranObj = genLevel('test')
    app.terrain = app.terranObj.terrainArray(app)

    # Instantiate Mario ##########################################
    cx, cy, health, height, width = app.width/2, app.height/2, 5, 80, 50
    app.playerMario = Mario(cx, cy, health, height, width)
    app.marioCx = app.playerMario.getCx()
    app.marioCy = app.playerMario.getCy()
    app.marioH = app.playerMario.getHeight()
    app.marioW = app.playerMario.getWidth()
    app.marioHealth = app.playerMario.getHealth()

    app.jumping = False
    app.jumpTime = 0

    # Instantiate enemies ##########################################


    # Instantiate bulletBills ##########################################

    app.bulletBill = bulletBill(2)

def appStopped(app):
    app.messages.append('appStopped')
    print('appStopped!')

runApp(width=600, height=600)
