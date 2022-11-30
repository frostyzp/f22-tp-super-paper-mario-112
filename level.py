import random
import os
import bisect 
from PIL import Image, ImageDraw
from cmu_112_graphics import *
import math


##########################################
# Terrain generator across 2d lists
##########################################

# With reference to https://bitesofcode.wordpress.com/2016/12/23/landscape-generation-using-midpoint-displacement/
def midpointDisplacement(start, end, roughness, verticalDisplacement=None, iterations=2):
    # Data structure that stores the points is a list of lists where
        # Each sublist represents a point and holds its x and y coordinates:
        points = [start, end]
        iteration = 1
        while iteration <= iterations:
            points_tup = tuple(points)
            # Calculate x and y midpoint coordinates:
            # [(x_i+x_(i+1))/2, (y_i+y_(i+1))/2]
            for i in range(len(points_tup)-1):
                midpoint = list(map(lambda x: (points_tup[i][x]+points_tup[i+1][x])/2,
                                    [0, 1]))
                # Displace midpoint y-coordinate
                midpoint[1] += random.choice([-verticalDisplacement,
                                            verticalDisplacement])
                # Insert the displaced midpoint in the current list of points         
                bisect.insort(points, midpoint)
            # Reduce displacement range
            verticalDisplacement *= 2 ** (-roughness)
            # Update number of iterations
            iteration += 1
        return points

class genLevel(object):
    def __init__(self, iterations):
        self.iterations = iterations

    # With reference from https://arpit.substack.com/p/1d-procedural-terrain-generation
    def generateTerrainArray(self):

        rows = 30 # terrain height
        cols = 480 # terrain width

        # x0, y0 and x1, y1 | roughness | vertical displacement | iterations
        midpointTerrain = midpointDisplacement([0, 24], [cols, 28], 0.05, 2, self.iterations)
        print(midpointTerrain)

        ######### Translating generated points into terrain ##########
        # Initialize 2d list which will contain and draw 'terrain'
        terrain = [(cols * [0]) for r in range(rows)]

        # Bounds check for 2d list, and ensure purposeful terrain generation
        # can be drawn onto the game
        for (x, y) in midpointTerrain:
            x = math.floor(int(x))
            y = math.floor(int(y))
            if x >= cols or x < 0:
                x = min(cols - 1, x)
            if y >= rows or y < 0:
                y = min(rows - 2, y)
            
            # Draw varied platforms - long, or combined
            # self.iterations is only > 5 if gameDifficulty is Easy
            # Will not draw random platforms if gameDifficulty is Easy
            randoSeed = random.randint(1, 10)
            if randoSeed >= 3 or self.iterations > 5:
                # Draw platform and tiles to bottom of the screen (tube-like)
                for i in range(random.randint(7,10)):
                    if x + i < cols:
                        terrain[y][x + i] = 'ground'
                        for ground in range(y + 1, rows):
                            terrain[ground][x + i] = 'ground'
            else:
                # Only draw platform itself
                for i in range(random.randint(6,9)):
                    if x + i < cols:
                        terrain[y][x + i] = 'ground'
        
        return terrain

    def drawTerrain(self, app, canvas):
    # Draw the terrain, which moves along scrollX
    # Max height, width
        for tRow in range(app.rows):
        # Draw only what needs to be displayed at the time
        # According to 30 x 30 tile (600 x 600 game)
            for tCol in range(app.cols + app.scrollX // 15):
                (x0, y0, x1, y1) = getCellBounds(app, tRow, tCol)
                if app.terrain[tRow][tCol] == 'ground':
                    x0 -= app.scrollX
                    x1 -= app.scrollX
                    canvas.create_rectangle(x0, y0, x1, y1, fill= 'green3', outline = 'darkgreen')
                elif app.terrain[tRow][tCol] == 'belowGround':
                    x0 -= app.scrollX
                    x1 -= app.scrollX
                    brown = 'darkorange4'
                    canvas.create_rectangle(x0, y0, x1, y1, fill= brown, outline = 'black')

        # Draw door at the end (win game condition)
        if app.scrollX > app.winScrollXDist - 200:
            canvas.create_image((app.width), app.height/2, 
            image = ImageTk.PhotoImage(app.doorWin))

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

    