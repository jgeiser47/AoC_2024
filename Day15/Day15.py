'''
    What: Advent of Code 2024 - Day 15
    Who: Josh Geiser
'''

from pathlib import Path
from typing import List, Tuple, Dict

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Coord():
    ''' Helper class for defining a (row, col) position '''
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def toTuple(self):
        return (self.r, self.c)
    
    def getNeigh(self, move:str):
        ''' Get a Coord object for adjacent neighbor in "move" direction '''
        if   move == '^': return Coord(self.r - 1, self.c)
        elif move == 'v': return Coord(self.r + 1, self.c)
        elif move == '>': return Coord(self.r, self.c + 1)
        elif move == '<': return Coord(self.r, self.c - 1)
        else:             raise SystemError()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Grid():
    ''' Helper class for storing properties of our grid '''

    def __init__(self, inputs, part2=False):
        self.grid = []

        # For part1, basically just make a 2D array
        if not part2:
            for input in inputs:
                self.grid.append([ch for ch in input])
        
        # For part 2, we gotta do a little bit of extra processing
        else:
            for input in inputs:
                listOfTups = [self.__p2(ch) for ch in input]
                self.grid.append([ch for tup in listOfTups for ch in tup])

        # Also initialize with our grid dimensions and robot location
        self.M = len(self.grid)
        self.N = len(self.grid[0])
        self.robot = None

    def __p2(self, ch:str) -> Tuple[str, str]:
        ''' Helper for initializing our grid in part 2 '''
        if   ch == '#': return ('#', '#')
        elif ch == 'O': return ('[', ']')
        elif ch == '.': return ('.', '.')
        elif ch == '@': return ('@', '.')
        else:           raise SystemError()

    def __contains__(self, coord:Coord) -> bool:
        ''' So that we can do things like: if coord in grid '''
        return 0 <= coord.r < self.M and 0 <= coord.c < self.N
    
    def getValAt(self, coord:Coord) -> str:
        return self.grid[coord.r][coord.c]
    
    def setValAt(self, coord:Coord, val:str):
        self.grid[coord.r][coord.c] = val
        return
    
    def moveFromTo(self, fromCoord:Coord, toCoord:Coord):
        ''' Given a from coordinate and a to coordinate, complete our move '''

        # These should always be true, might be a bug in our logic if not
        assert self.getValAt(toCoord) == '.'
        assert self.getValAt(fromCoord) in {'@', 'O'}

        # Reset location of objects accordingly 
        self.setValAt(toCoord, self.getValAt(fromCoord))
        self.setValAt(fromCoord, '.')

        # If our robot is involved, also reset its location
        if self.getValAt(toCoord) == '@':
            self.robot = Coord(toCoord.r, toCoord.c)

        return
    
    def getRobot(self):
        ''' Return Coord object of our robot's current location '''
        if self.robot is None:
            for r in range(self.M):
                for c in range(self.N):
                    if self.grid[r][c] == '@':
                        self.robot = Coord(r,c)

        return self.robot
    
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def parseInputs(inputs:List[str], part2=False) -> Tuple[Grid, str]:
    ''' Helper for parsing our inputs into a Grid object and a lit of moves '''

    iBreak = [i for i,input in enumerate(inputs) if len(input) == 0][0]
    grid = Grid(inputs[:iBreak], part2=part2)
    moves = ''.join(inputs[iBreak+1:])

    return grid, moves

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def attemptMove(grid:Grid, move:str):
    ''' Attempt our move (for part 1) only '''

    # We need to make a stack of potential coordinates to be moved
    stack = []

    # Current robot's location
    robotCoord = grid.getRobot()
    stack.append(robotCoord)

    # Location we're trying to move to
    nextCoord = robotCoord.getNeigh(move)
    stack.append(nextCoord)

    # As long as we've got a string of boxes, keep checking next location in same direction
    while grid.getValAt(nextCoord) == 'O':
        nextCoord = nextCoord.getNeigh(move)
        stack.append(nextCoord)

    # If we've reached a wall, we can't complete this move, so return with no side effects
    if grid.getValAt(nextCoord) == '#':
        return
    
    # If we've reached an open space, then complete our move!
    if grid.getValAt(nextCoord) == '.':

        # Basically just move our objects one at a time
        while len(stack) > 1:
            moveToCoord = stack.pop()
            moveFromCoord = stack[-1]
            grid.moveFromTo(moveFromCoord, moveToCoord)

        return

    # Hope we don't get here...
    raise SystemError()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getScore(grid:Grid) -> int:
    ''' Return the "score" of the grid (after all moves are completed) '''

    out = 0
    for r in range(grid.M):
        for c in range(grid.N):
            if grid.getValAt(Coord(r,c)) == 'O':
                out += 100 * r + c

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Do the thing!
    grid, moves = parseInputs(inputs)
    for move in moves:
        attemptMove(grid, move)

    return getScore(grid)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def attemptMove2(grid:Grid, move:str):
    ''' Attempt our move (for part 1) only '''

    # We need to make a stack of potential coordinates to be moved
    stack = []

    # Current robot's location
    robotCoord = grid.getRobot()
    stack.append(robotCoord)

    # Location we're trying to move to
    nextCoord = robotCoord.getNeigh(move)
    stack.append(nextCoord)

    # As long as we've got a string of boxes, keep checking next location in same direction
    while grid.getValAt(nextCoord) == 'O':
        nextCoord = nextCoord.getNeigh(move)
        stack.append(nextCoord)

    # If we've reached a wall, we can't complete this move, so return with no side effects
    if grid.getValAt(nextCoord) == '#':
        return
    
    # If we've reached an open space, then complete our move!
    if grid.getValAt(nextCoord) == '.':

        # Basically just move our objects one at a time
        while len(stack) > 1:
            moveToCoord = stack.pop()
            moveFromCoord = stack[-1]
            grid.moveFromTo(moveFromCoord, moveToCoord)

        return

    # Hope we don't get here...
    raise SystemError()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Do the thing (part 2 style)!
    grid, moves = parseInputs(inputs, part2=True)
    for move in moves:
        attemptMove2(grid, move)

    return getScore(grid)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

    infile = Path(__file__).parent / 'sample.txt'

    # inputs = read_input(infile)
    # print(task_1(inputs))

    inputs = read_input(infile)
    print(task_2(inputs))

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
    main()
