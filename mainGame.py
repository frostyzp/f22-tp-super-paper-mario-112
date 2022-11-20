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
    elif (event.key == 'd'):
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

    # ## With reference from 112 notes - 
    # for r in range(app.rows):
    #     for c in range(app.cols):
    #         (x0, y0, x1, y1) = getCellBounds(app, r, c)
    #         canvas.create_rectangle(x0, y0, x1, y1, fill='')

    # Draw random platforms here
    # for (cx, cy) in app.platforms:

def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def drawMario(app, canvas):
    # Draw sprite image of mario here
    # runningLeft, runningRight, jumping,
    # x1, y1 (top left), x2, y2 (bottom left)

    # canvas.create_oval(app.marioCx-app.marioW, app.marioCy-app.marioH, 
    # app.marioCx+app.marioW, app.marioCy+app.marioH, fill='cyan')

    canvas.create_oval(app.marioCx, app.marioCy, app.marioCx - app.marioW,
    app.marioCy - app.marioH, fill='red')

def drawTerrain(app, canvas):
    # Draw the terrain, which moves along scrollX
    # Max height, width
    # for (tX, tY, tLength) in app.terrain:
    for tRow in range(app.rows):
        for tCol in range(app.cols):
        # tLength -= app.scrollX
        # tY += app.scrollY
        # Draw image here
        # canvas.create_rectangle(tX, tY, tX + tLength, app.height, 
        # fill='lightGreen')
            if app.terrain[tRow][tCol] == 'tile':
                (x0, y0, x1, y1) = getCellBounds(app, tRow, tCol)
                x0 -= app.scrollX
                x1 -= app.scrollX
                canvas.create_rectangle(x0, y0, x1, y1, fill= 'yellow')

        # for (cx, cy) in app.dots: ###########################
        # cx -= app.scrollX  # <-- This is where we scroll each dot!!!
        # canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='lightGreen')

    # app.rows += app.scrollX - MVC violation
    # move the data in the 2d list?

def drawStats(app, canvas):
    canvas.create_text(50, 20,
    text= f'{app.playerMario.getHealth()}', fill = 'yellow', font=f'Arial {20} bold')
    canvas.create_text(app.width/2, 20,
    text= f'{app.gameMode}', fill = 'yellow', font=f'Arial {20} bold')


def gameMode_keyPressed(app, event):
    if (event.key == 'h'):
        app.mode = 'helpMode'
    if (event.key == "Left"): 
        # Start screen (left) constraint ##############
        if app.scrollX > -10:
            app.scrollX -= app.playerMario.getRunSpeed()
            app.scrollXObj -= 1

    elif (event.key == "Right"): 
        app.scrollX += app.playerMario.getRunSpeed()
        app.scrollXObj += 1
    elif (event.key == "Up"): 
        print("JUMP!")
        # Gravity / jump
        app.jumping = True

def gravity(app):
    yGravity = 15
    if app.jumping == False:
        app.marioCy += yGravity

def groudCollision(app, tX, tY):
    # Check to see if there are any collisions with the ground
    # Gravity is applied when there is no collision detected
    # tX += app.scrollY

    # if app.marioCy > tY: #and app.marioCx + app.marioW > cx:
    #     return True
    # elif app.marioCx > tX:
    #     return True
    # return False
    pass
   
def gameMode_timerFired(app):
    app.jumpHeight = 5

    # Ground collision detection
    print('Terrain[y/height][x/rows],', math.ceil(app.marioCy / 20),math.ceil(app.marioCx / 20 - app.scrollXObj))
    print(app.terrain[math.ceil(app.marioCy / 20)][abs(math.ceil(app.marioCx / 20))])
    # terrain[row][col] -- shouuld only be up to 30...

    # If marioPos in 2d list is tile (drawn as yellow squares), then there is collision 
    # 20 pixels for each of the 30 tiles = 600 x 600 screen
    if app.terrain[math.ceil(app.marioCy / 20)][abs(math.ceil(app.marioCx / 20))] != 'tile':
        print("######### No collision with ground #######ss####")
        gravity(app)


    app.jumpHeight = 10
    app.velocityJump = app.jumpHeight
 
    # Jump with Gravity
    if app.jumping == True:
        # How long mario is in the air
        app.jumpTime += 1
        app.marioCy -= 20
        #char.upwardsvelocity
    if app.jumpTime == 5:
    #     # if groudCollision(app, tX, tY) == False:
    #         app.marioCy += 12
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
    app.scrollXObj = 0

    app.cols = 30
    app.rows = 30
    app.margin = 5

    # 60 x 60 grid of 10
    app.screenTiles = [ ([''] * app.cols) for i in range(app.rows)]


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
    # app.marioPos = [app.marioCx][app.marioCy]

    app.jumping = False
    app.jumpTime = 0

    # Instantiate enemies ##########################################


    # Instantiate bulletBills ##########################################
    app.bulletBill = bulletBill(2)

def appStopped(app):
    app.messages.append('appStopped')
    print('appStopped!')

runApp(width=600, height=600)
