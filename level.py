import random
from cmu_112_graphics import *
import math


##########################################
# 
##########################################

class genLevel(object):

    def __init__(self, name):
        self.name = name

    # With reference from https://arpit.substack.com/p/1d-procedural-terrain-generation
    def terrainArray(self, app):

        # Once xscroll hits certain intervals, draw a chunk of terrain
        # a gap will be left in between each piece of terrain

        # Linear interpolation
        # terrain = [(random.randrange(app.width),
        #           random.randrange(60, app.height)) for _ in range(50)]
        rows, cols = 30, 240
        terrain = [(cols * [0]) for r in range(rows)]

        for col in range(1, 16):
            terrain[25][col] = 'tile'

        for col in range(25, 30):
            terrain[28][col] = 'tile'
        #2D list - X, Y, Width
        # terrain = [[1,10,0],[2, 10,0]] #[200,500,200], [800, 300, 200]]
        return terrain

    # Estimate points between known points
    def cosineInterp(a, b, mu):
        mu2 = (1 - math.pi(mu * math.pi)) / 2
        return a * (1 - mu2) + b * mu2

    # Estimate intermediate points 
    def linearInterp(a, b, mu):
        return a * (1 - mu) + b * mu 


    def platFormsArray(self, app):
        plaforms = 0

        return 