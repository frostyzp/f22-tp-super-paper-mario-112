import random
from cmu_112_graphics import *
import math

##########################################
# Terrain generator across 2d lists
##########################################

class genLevel(object):
    rows = 30
    cols = 240
    rawTerrain = [(240 * [0]) for r in range(rows)]

    def __init__(self, platforms):
        self.platforms = platforms

    # With reference from https://arpit.substack.com/p/1d-procedural-terrain-generation
    def terrainArray(self, app):
        # Once xscroll hits certain intervals, draw a chunk of terrain
        # a gap will be left in between each piece of terrain

        rows, cols = 30, 240
        terrain = [(cols * [0]) for r in range(rows)]

        for col in range(1, 16):
            terrain[25][col] = ''

        for col in range(25, 30):
            terrain[28][col] = ''
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

 # With reference from https://bitesofcode.wordpress.com/2016/12/23/landscape-generation-using-midpoint-displacement/

 