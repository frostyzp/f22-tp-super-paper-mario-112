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
    canvas.create_image(app.width/2-200,app.height/2+100, 
    image= ImageTk.PhotoImage(app.splashMarioBgS))
    canvas.create_image(app.width/2+200,app.height/2, 
    image= ImageTk.PhotoImage(app.splashLuigiBg))

    # Instructions on Splash - S for Easy, D for Hard
    canvas.create_text(app.width/2, 400, text='Press D for Easy mode',
                       font=font, fill='white')
    canvas.create_text(app.width/2, 450, text='Press H for Help',
                       font=font, fill='white')

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
    # for row in range(app.rows):
    #     for col in range(app.cols):
    #         (x0, y0, x1, y1) = getCellBounds(app, row, col)
    #         canvas.create_rectangle(x0, y0, x1, y1,
    #                                 fill='white', outline='black')


    drawMario(app, canvas)
    
    drawTerrain(app, canvas)
    drawStats(app, canvas)

    drawBulletBill(app, canvas)

    # Draw random platforms here
    # for (cx, cy) in app.platforms:

# Referenced from 112 - https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#sidescrollerExamples
def getCellBounds(app, row, col):
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
    (x0, y0, x1, y1) = app.playerMario.getBounds()

    # canvas.create_rectangle(app.playerMario.x - app.scrollX, app.playerMario.y,
    # app.playerMario.x - app.scrollX + app.playerMario.width, app.playerMario.y - app.playerMario.height, 
    # fill='red')
    canvas.create_rectangle(x0 - app.scrollX, y0 + 40, x1 - app.scrollX, y1 + 40, 
    fill='red')

    sprite = app.sprites[app.spriteCounter]
    canvas.create_image(x0 - app.scrollX, y0 + 40, image=ImageTk.PhotoImage(sprite))

def drawTerrain(app, canvas):
    # Draw the terrain, which moves along scrollX
    # Max height, width
    # for (tX, tY, tLength) in app.terrain:
    for tRow in range(app.rows):
        for tCol in range(app.cols):
        # Draw tile from images here
            (x0, y0, x1, y1) = getCellBounds(app, tRow, tCol)
            # canvas.create_rectangle(x0, y0, x1, y1, outline='black')
            # if app.terrainObj.terrainArray(app)[tRow][tCol] == '':
            if app.terrainObj.rawTerrain[tRow][tCol] == '':
                print(app.terrainObj.rawTerrain[tRow][tCol])
                x0 -= app.scrollX
                x1 -= app.scrollX
                canvas.create_rectangle(x0, y0, x1, y1, fill= 'lime green')

def drawStats(app, canvas):
    font = 'MARIOFontv3_2-Solid 20 bold'
    # Stats - Health, gameMode (easy/hard), Score (points)
    canvas.create_image(60, 30, image= ImageTk.PhotoImage(app.heartImgs))

    canvas.create_text(70, 25,
    text= '  / 5', fill = 'white', font=font)
    canvas.create_text(55, 25,
    text= f'{app.playerMario.getHealth()}', fill = 'white', font=font)

    canvas.create_text(app.width/2, 25,
    text= f'{app.gameMode}', fill = 'white', font=font)

    canvas.create_text(app.width-50, 25,
    text= f'{app.points}', fill = 'white', font=font)

def gameMode_keyPressed(app, event):
    if (event.key == 'h'):
        app.mode = 'helpMode'

# Mario with RESPECT TO THE GAME - MARIO 0 0 IS THE - CONSISTENT VARS 
    if (event.key == "Left"): 
        # Start screen (left) constraint ##############
        if app.scrollX > -10:
            app.scrollX -= app.playerMario.getRunSpeed()
            app.playerMario.x -= app.playerMario.getRunSpeed()

    elif (event.key == "Right"): 
        app.scrollX += app.playerMario.getRunSpeed()
        app.playerMario.x += app.playerMario.getRunSpeed()
        app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)


    elif (event.key == "Up"): 
        print("JUMP!")
        # Gravity / jump
        app.jumping = True

def gravity(app):
    yGravity = 20
    if app.jumping == False:
        app.playerMario.y += yGravity
   
def gameMode_timerFired(app):
    # Ground collision detection
    print('marioY,marioX', math.floor(app.playerMario.y / 20), math.floor(app.playerMario.x / 20))
    # 20 pixels for each of the 30 tiles = 600 x 600 screen


    # Terrain colision check -- turn on gravity
    if app.playerMario.collisionHit(app.terrainObj.terrainArray(app)) == False:
        gravity(app)

    # Jump!
    app.jumpHeight = 10
    app.velocityJump = app.jumpHeight
    playerJump(app)
    loseGame(app)
    winGame(app)

    # Add bulletBill to a list, every x frequency
    app.bulletFreq += 1
    # Create bullet objects, add them to a list
    spawnBulletBill(app)

    # Bullet collision detection
    # if app.playerMario.collisionHit(app.gameGrid):

    # Increase cx of projectiles
    for bullet in app.bulletBillList:
        bullet.x -= 15
        print('bulletBounds,', bullet.getBounds())
        print('marioBounds', app.playerMario.getBounds())
        if boundsIntersect(app, app.playerMario.getBounds(), bullet.getBounds()):
            print(app.playerMario.getBounds(), bullet.getBounds())
            app.playerMario.health -= 1
            # bullet.x = app.width
            print('BULLET HIT ############################')
            # app.bulletBillList.pop(bullet)
        if bullet.x < 0:
            pass

    

def spawnBulletBill(app):
    i = 0
    if (app.bulletFreq % 15 == 0):
        newBullet = bulletBill(app.playerMario.x + (15 * 20), random.randint(24,25) * 20, 
        app.bulletDamage)
        # [i] = 
        i += 1
        app.bulletBillList.append(newBullet)
        # print("BULLET BILLLL", math.floor(newBullet.y / 20), math.floor(newBullet.x / 20))
        # app.gameGrid[math.floor(newBullet.y / 20)][math.floor(newBullet.x / 20)] = ''
        # app.bulletBillList.append(newBullet[newBullet.cx][newBullet.cy])
        # print(app.bulletBillList) # DEBUG!


def boundsIntersect(app, boundsA, boundsB):
    # return l2<=r1 and t2<=b1 and l1<=r2 and t1<=b2
    (ax0, ay0, ax1, ay1) = boundsA
    (bx0, by0, bx1, by1) = boundsB
    # return ((ax1 == bx0) and (bx1 == ax0) and
    #         (ay1 == by0) and (by1 == ay0))
    return ((ax1 >= bx0) and (bx1 >= ax0) and
            (ay1 >= by0) and (by1 >= ay0))


def playerJump(app):
        # Jump with Gravity
    if app.jumping == True:
        # How long mario is in the air
        app.jumpTime += 1
        app.playerMario.y -= 20

    if app.jumpTime == 5:
            app.jumping = False
            app.jumpTime = 0

def loseGame(app):
    if math.floor(app.playerMario.y / 20) >= app.cols or app.playerMario.health == 0:
        app.mode = 'gameOverMode'

        
def winGame(app):
    if app.scrollX == 239:
        app.mode = 'gameWinMode'


def drawBulletBill(app, canvas):
    # Loop through all bullet bills, and draw them on the canvas
    for bullets in app.bulletBillList:
        bullets.redraw(app, canvas)

##########################################
# Help Mode
##########################################

def helpMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'

    canvas.create_image(app.width/2,app.height/2, 
    image= ImageTk.PhotoImage(app.sideSplashBgS))

    canvas.create_text(app.width/2, 150, text='Help Screen', 
                       font=font, fill='white')
    canvas.create_text(app.width/2, 250, text='Press R to restart',
                       font=font, fill='white')
    canvas.create_text(app.width/2, 350, text='Press any key to return to the game!',
                       font=font, fill='white')

def helpMode_keyPressed(app, event):
    app.mode = 'gameMode'

##########################################
# GameOver Mode
##########################################

def gameOverMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2,app.height/2, 
    image= ImageTk.PhotoImage(app.sideSplashBgS))
    font = 'Arial 30 bold'
    subtitle = 'Arial 20'

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
    app.playerMario.y = app.height/2
    app.playerMario.x = app.width/2
    app.scrollX = 0
    app.points = 0
    app.bulletBillList = []
    app.playerMario.heart = 5

##########################################
# GameWin Mode
##########################################

def gameWinMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'

    canvas.create_image(app.width/2,app.height/2, 
    image= ImageTk.PhotoImage(app.sideSplashBgS))

    canvas.create_text(app.width/2, 150, text='You saved Luigi!', 
                       font=font, fill='black')
    canvas.create_text(app.width/2, 250, text='R to restart',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 350, text='B to go back',
                       font=font, fill='black')

    # canvas.create_text(app.width/2, 350, text=f' You earnt {app.points} points',
    #                    font=font, fill='black')

def gameOverMode_keyPressed(app, event):
    if (event.key == 'r'):
            app.mode = 'gameMode'
            resetGame(app)
    elif (event.key == 'b'):
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
    app.gameMode = 'Easy'

    app.scrollX = 0

    app.cols = 30
    app.rows = 30
    app.margin = 5
    
    # Stats for the game
    app.points = 0

    # 30 x 30 grid of 20 for main game screen
    app.screenTiles = [ ([''] * app.cols) for i in range(app.rows)]

    ##########################################
    # Images from https://www.mariowiki.com/Gallery:Super_Paper_Mario 
    app.starterBg = createImg(app, 'images/gameBg.jpg', 1)
    app.splashBgS = createImg(app, 'images/splash/splashBg.png', 4/5)

    # app.titleSplash = app.loadImage('images/splash/titleSplash.png')
    # app.titleSplashS = app.scaleImage(app.titleSplash, 1/3)
    app.titleSplashS = createImg(app, 'images/splash/titleSplash.png', 1/3)

    # app.sideSplashBg = app.loadImage('images/splash/sideSplash.png')
    # app.sideSplashBgS = app.scaleImage(app.sideSplashBg, 9/10)
    app.sideSplashBgS = createImg(app, 'images/splash/sideSplash.png', 9/10)

    # app.splashMarioBg = app.loadImage('images/splash/marioSplash.png')
    # app.splashMarioBgS = app.scaleImage(app.splashMarioBg, 2/3)
    app.splashMarioBgS = createImg(app, 'images/splash/marioSplash.png', 2/3)

    app.splashLuigiBg = app.loadImage('images/splash/luigiSplash.png')
    app.splashLuigiBgS = app.scaleImage(app.splashLuigiBg, 1/10)
    app.splashMarioBgS = createImg(app, 'images/splash/marioSplash.png', 2/3)


    app.bulletBillImg = app.loadImage('images/characters/bulletBill.png')
    app.bulletBillImgS = app.scaleImage(app.bulletBillImg, 2/5)

    # Images from https://www.spriters-resource.com/wii/superpapermario/ 
    app.heartImg = app.loadImage('images/heart.png')
    app.heartImgs = app.scaleImage(app.heartImg, 1/11)

    # With reference from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
    # Sprite images - 1440 x 360 - 480 / still  
    # Scaled down sprite images -- 576 x 144 - 192
    spritestripWalkR = app.loadImage('images/characters/marioWalkR.png')
    spriteWalkR = app.scaleImage(spritestripWalkR, 2/5)
    spritestripWalkR = app.loadImage('images/characters/marioWalkR.png')
    spriteWalkR = app.scaleImage(spritestripWalkR, 2/5)
    
    app.sprites = [ ]
    for i in range(3):
        sprite = spriteWalkR.crop((10+192*i, 10, 182+192*i, 144))
        app.sprites.append(sprite)
    app.spriteCounter = 0

    # marioWalkL.png / marioJumpR.png marioJumpL.png



    # Instantiate Terrain ##########################################
    app.terrainObj = genLevel(5)

    # Instantiate Mario ##########################################
    x, y, health, height, width = app.width/2, app.height/2, 5, 40, 20
    app.playerMario = Mario(x, y, health, height, width)

    app.jumping = False
    app.jumpTime = 0

    # Instantiate enemies ##########################################


    # Instantiate bulletBills ##########################################
    app.bulletFreq = 0
    app.bulletBillList = []
    app.bulletDamage = 2

def appStopped(app):
    app.messages.append('appStopped')
    print('appStopped!')

runApp(width=600, height=600)
