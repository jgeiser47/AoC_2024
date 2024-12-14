'''
    What: Advent of Code 2024 - Day 14
    Who: Josh Geiser
'''

from pathlib import Path
from typing import List, Dict
import math

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Coord():
    ''' Helper class for defining an (X, Y) position or velocity'''
    def __init__(self, x, y):
        self.x = x
        self.y = y

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Robot():
    ''' Helper class for defining a robot with position and velocity '''
    def __init__(self, line):
        self.pos = Coord(*[int(x) for x in line.split(' ')[0][2:].split(',')])
        self.vel = Coord(*[int(x) for x in line.split(' ')[1][2:].split(',')])

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def parseInputs(inputs:str) -> List[Robot]:
    ''' Pre-process our inputs into a list of robots '''

    robots = []
    for input in inputs:
        robots.append(Robot(input))

    return robots

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getRobotFinalPos(robot:Robot, WIDTH:int, HEIGHT:int, TIME:int) -> Coord:
    ''' Get the robot's final position coordinate at a given time '''

    finalX = (robot.pos.x + (robot.vel.x * TIME)) % WIDTH
    finalY = (robot.pos.y + (robot.vel.y * TIME)) % HEIGHT

    return Coord(finalX, finalY)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getQuad(finalPos:Coord, quad:Dict[str, int], WIDTH:int, HEIGHT:int):
    ''' Based on position coordinate, determine what quad (if any) we're in '''

    # Midpoints in vertical and horizontal dimensions
    midVert = int(WIDTH / 2)
    midHoriz = int(HEIGHT / 2)

    # NW quad
    if (0 <= finalPos.x < midVert and 0 <= finalPos.y < midHoriz):
        quad['NW'] += 1 

    # NE quad
    elif (midVert < finalPos.x < WIDTH and 0 <= finalPos.y < midHoriz):
        quad['NE'] += 1

    # SW quad
    elif (0 <= finalPos.x < midVert and midHoriz < finalPos.y < HEIGHT):
        quad['SW'] += 1

    # SE quad
    elif (midVert < finalPos.x < WIDTH and midHoriz < finalPos.y < HEIGHT):
        quad['SE'] += 1

    # No quad! (on midlines)
    return 

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Get our inputs
    robots = parseInputs(inputs)

    # If true, use sample.txt dimensions, else input.txt dimensions
    if robots[0].pos.x == 0:
        WIDTH = 11
        HEIGHT = 7
        TIME = 100
    else:
        WIDTH = 101
        HEIGHT = 103
        TIME = 100

    # How many robots are in each quad
    quads = {
        'NW' : 0,
        'NE' : 0,
        'SW' : 0,
        'SE' : 0
    }

    # Simulate all robots and add to quads
    for robot in robots:
        finalPos = getRobotFinalPos(robot, WIDTH, HEIGHT, TIME)
        getQuad(finalPos, quads, WIDTH, HEIGHT)

    # Now just multiply quads together
    return math.prod(list(quads.values()))

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Get our inputs
    robots = parseInputs(inputs)

    # If true, use sample.txt dimensions, else input.txt dimensions
    if robots[0].pos.x == 0:
        WIDTH = 11
        HEIGHT = 7
    else:
        WIDTH = 101
        HEIGHT = 103

    # Just simulate for awhile...
    for time in range(1000000):

        # 2D array defining robot positions
        grid = [['.' for i in range(WIDTH)] for j in range(HEIGHT)]
        for robot in robots:
            finalPos = getRobotFinalPos(robot, WIDTH, HEIGHT, time)
            grid[finalPos.y][finalPos.x] = '#'

        # Now squash our 2D array into a single string
        gridSquashedStr = ''.join([''.join(x) for x in grid])

        # Check if that string has a long line of ######## values which means
        # a lot of robots in a horizontal row (i.e., bottom portion of tree)
        if '##########' in gridSquashedStr:
            return time
        
        # Just to show how many iterations we've gone through...
        if time % 1000 == 0:
            print(f'Time: {time}')

    # Yikes if we've gotten here...
    raise SystemError()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

    infile = Path(__file__).parent / 'input.txt'

    inputs = read_input(infile)
    print(task_1(inputs))

    inputs = read_input(infile)
    print(task_2(inputs))

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
    main()
