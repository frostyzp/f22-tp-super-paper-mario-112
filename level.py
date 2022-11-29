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
def midpointDisplacement(start, end, roughness, verticalDisplacement=None, iterations=2, recursive=4):
    # Data structure that stores the points is a list of lists where
        # Each sublist represents a point and holds its x and y coordinates:
        points = [start, end]
        iteration = 1
        while iteration <= iterations:
            # Tuple to hold start and end points, as immutable data storage
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
                # bisect allows to insert an element in a list so that its order
                # is preserved.

            # Reduce displacement range
            verticalDisplacement *= 2 ** (-roughness)
            # Update number of iterations
            iteration += 1
        return points

class genLevel(object):
    def __init__(self, platforms):
        self.platforms = platforms

    # With reference from https://arpit.substack.com/p/1d-procedural-terrain-generation
    def generateTerrainArray(self):

        rows = 30 # terrain height
        cols = 480 # terrain width
        
        # x0, y0 and x1, y1 | roughness | vertical displacement | iterations
        
        midpointTerrain = midpointDisplacement([0, 24], [cols, 25], 0.5, 2, 5)
        # cols will be split into chunks -- 120 * 4
        
        print(midpointTerrain)

        ######### Translating generated points into terrain ##########
        # Initialize 2d list which will contain and draw 'terrain'
        terrain = [(cols * [0]) for r in range(rows)]

        for (x, y) in midpointTerrain:
            x = math.floor(int(x))
            y = math.floor(int(y))
            # Bounds check for 2d list, and ensure purposeful terrain generation
            # can be drawn onto the game
            if x >= cols or x < 0:
                x = min(cols - 1, x)
            if y >= rows or y < 0:
                y = min(rows - 2, y)
            
            # Create platforms of various lengths, based on midpoints returned
            for i in range(random.randint(6,9)):
                if x + i < cols:
                    terrain[y][x + i] = 'ground'
                    for ground in range(y + 1, rows):
                        terrain[ground][x + i] = 'belowGround'


            # Draw image of the doors to indicate the end of the game
            # Win condition!
        return terrain

    def platFormsArray(self, terrain):
        # Will generate on only one y axis
        for i in range(0, self.platform):
            # random x values, but ensure there are no overlaps
            x = 50
            # generate platforms of length 5
            for col in range(x, x+5):
                terrain[col][20] = ''

        return terrain

