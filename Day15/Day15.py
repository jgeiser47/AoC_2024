'''
    What: Advent of Code 2024 - Day 15
    Who: Josh Geiser
'''

from pathlib import Path
from typing import List, Tuple

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

    def getOtherHalf(self, val:str):
        ''' For part 2: get the coordinate of the other half of the box '''
        return self.getNeigh('>') if val == '[' else self.getNeigh('<')

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
        assert self.getValAt(fromCoord) in {'@', 'O', '[', ']'}

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
    ''' Helper for parsing our inputs into a Grid object and a list of moves '''

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
def getScore(grid:Grid, part2=False) -> int:
    ''' Return the "score" of the grid (after all moves are completed) '''

    boxStr = 'O' if not part2 else '['

    out = 0
    for r in range(grid.M):
        for c in range(grid.N):
            if grid.getValAt(Coord(r,c)) == boxStr:
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
def attemptHorizMove(grid:Grid, move:str):
    ''' Attempt a horizontal move (for part 2) only '''

    # We need to make a stack of potential coordinates to be moved
    stack = []

    # Current robot's location
    robotCoord = grid.getRobot()
    stack.append(robotCoord)

    # Location we're trying to move to
    nextCoord = robotCoord.getNeigh(move)
    stack.append(nextCoord)

    # As long as we've got a string of boxes, keep checking next location in same direction
    while grid.getValAt(nextCoord) in {'[', ']'}:
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
def attemptVertMove(grid:Grid, move:str):
    ''' Attempt a vertical move (part 2 only) '''

    # Stack of lists of potential coordinates to be moved
    stack = []

    # Current robot's location
    robotCoord = grid.getRobot()
    stack.append([robotCoord])

    # Each element in the stack will be it's own list of Coords for a given row index
    # If we visit a row of only empty spaces -> then we'll end up adding an empty list to our stack
    while len(stack[-1]) > 0:
        currRow = stack[-1]
        nextRow = []

        # Now for each element in the last row we visited, check each neighbor to the N or S
        for coord in currRow:
            neighbor = coord.getNeigh(move)

            # If our neighbor is part of a box, add both parts of the box to our list
            if grid.getValAt(neighbor) in {'[', ']'}:
                nextRow.append(neighbor)
                nextRow.append(neighbor.getOtherHalf(grid.getValAt(neighbor)))

            # If any part of our path is blocked by a wall, return immediately cuz we can't move!
            if grid.getValAt(neighbor) == '#':
                return

        # Now append our most recently visited row to the stack
        stack.append(nextRow)

    # Get rid of last element of stack, which should be an empty list (i.e., all empty spaces)
    stack.pop()

    # Now we need to actually complete our move
    while len(stack) > 0:
        currRow = stack.pop()

        # Potential for duplication when adding values in, just convert to stack to de-duplicate
        currRow = set([x.toTuple() for x in currRow])
        for coordTuple in currRow:
            coord = Coord(*coordTuple)

            # Use our Grid helper function to actually complete this move
            moveFromCoord = coord
            moveToCoord = moveFromCoord.getNeigh(move)
            grid.moveFromTo(moveFromCoord, moveToCoord)

    # Yay we're done!
    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Do the thing (part 2 style)!
    grid, moves = parseInputs(inputs, part2=True)
    for move in moves:
        if move in {'<', '>'}:
            attemptHorizMove(grid, move)
        else:
            attemptVertMove(grid, move)

    return getScore(grid, part2=True)

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
