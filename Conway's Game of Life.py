# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

import time
import random
import os
import sys

class Cell:
    def __init__(self):
        self.state = False
        self.sceduledState = False
        self.aliveNeighbours = 0


class World:
    def __init__(self, width, height):
        self.world = [[Cell() for i in range(width)] for j in range(height)]
        self.width = width
        self.height = height

        self.running = True
        self.generationsPassed = 0
        self.unstabilizingsnapshot = ""
        

    def start(self):
        self.running = True
        self.generationsPassed = 0
        self.unstabilizingsnapshot = ""
        
        while self.running:
            self.drawWorld()
            self.updateWorld()
            time.sleep(1/45)

    def calculateCellState(self, cellX, cellY):

        aliveNeighbours = 0

        offsetsToCheck = [  [-1, -1],   [-1, 0],    [-1, 1],
                            [0, -1],                [0, 1],
                            [1, -1],    [1, 0],     [1, 1]]

        for offset in offsetsToCheck:
            try:
                if self.world[cellX + offset[0]][cellY + offset[1]].state is True:
                    aliveNeighbours += 1
            except IndexError:
                pass
        try:
        
            if self.world[cellX][cellY].state is True:
                if aliveNeighbours == 2 or aliveNeighbours == 3:
                    self.world[cellX][cellY].sceduledState = True
                else:
                    self.world[cellX][cellY].sceduledState = False

            if self.world[cellX][cellY].state is False:
                if aliveNeighbours == 3:
                    self.world[cellX][cellY].sceduledState = True

            self.world[cellX][cellY].aliveNeighbours = aliveNeighbours
        except IndexError:
            pass

    def updateCellState(self, cellX, cellY):
        try:
            self.world[cellX][cellY].state = self.world[cellX][cellY].sceduledState
        except IndexError:
            pass

    def updateWorld(self):

        self.generationsPassed += 1
        
        for x in range(self.height):
            for y in range(self.width):
                self.calculateCellState(x, y)

        for x in range(self.height):
            for y in range(self.width):
                self.updateCellState(x, y)

    def drawWorld(self):

        output = ""

        for x in range(self.width):
            for y in range(self.height):
                if self.world[y][x].state is True:
                    output += u"\u2588" * 2
                else:
                    output += " " * 2
            if x != self.width - 1:
                output += "\n"
            
        # Reset if entirely full of blinkers
        if self.generationsPassed % 2:
            if output == self.unstabilizingsnapshot:
                self.running = False
            self.unstabilizingsnapshot = output

        sys.stdout.write(output)
        sys.stdout.flush()

mainWorld = World(30, 75)

for i in range(mainWorld.height):
    for j in range(mainWorld.width):
        if random.random() > 0.6:
            mainWorld.world[i][j].state = True


while True:
    mainWorld.start()
