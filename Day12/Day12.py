'''
    What: Advent of Code 2024 - Day 12
    Who: Josh Geiser
'''

from pathlib import Path
from queue import Queue
from typing import List, Set, Tuple

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Coord():
    ''' Helper class for giving us a coordinate on our grid '''
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def toTuple(self):
        return (self.r, self.c)

    def getNeigh(self, cardinal:str):
        ''' Return a Coord object in one of the four cardinal directions from us '''
        if   cardinal == 'N':   return Coord(self.r - 1, self.c)
        elif cardinal == 'S':   return Coord(self.r + 1, self.c)
        elif cardinal == 'W':   return Coord(self.r, self.c - 1)
        elif cardinal == 'E':   return Coord(self.r, self.c + 1)
        else:                   raise SystemError()

    def getOpenSides(self, region:Set[Tuple[int, int]]) -> Set[str]:
        ''' Get the sides from us that don't contain a neighbor '''
        sides = ['N','S','E','W']
        return set([side for side in sides if self.getNeigh(side).toTuple() not in region])

    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Grid():
    ''' Helper class for storing properties of our grid '''

    def __init__(self, grid):
        self.grid = grid
        self.M = len(grid)
        self.N = len(grid[0])

    def __contains__(self, coord:Coord) -> bool:
        ''' So that we can do things like: if coord in grid '''
        return 0 <= coord.r < self.M and 0 <= coord.c < self.N
    
    def valAt(self, coord:Coord) -> str:
        return self.grid[coord.r][coord.c]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def bfs(coord:Coord, grid:Grid, visited:set) -> Set[Tuple[int, int]]:
    ''' Perform breadth first search to get all of the coords in a region '''

    # Initialization 
    q = Queue()
    q.put(coord)
    regionSet = set()
    visited.add(coord.toTuple())
    regionChar = grid.valAt(coord)
    DIRS = [(-1, +0), (+1, +0), (+0, -1), (+0, +1)]

    # Start iterating until empty queue
    while not q.empty():

        # Get current coordinate from queue, check each direction
        coord = q.get()
        for dr, dc in DIRS:
            possNeigh = Coord(coord.r + dr, coord.c + dc)

            # If this neighbor hasn't been visited yet, add it to queue
            if (possNeigh in grid and 
                possNeigh.toTuple() not in visited and
                grid.valAt(possNeigh) == regionChar):

                visited.add(possNeigh.toTuple())
                q.put(possNeigh)
        
        # Anything that has been in the queue is part of our region
        regionSet.add(coord.toTuple())

    return regionSet

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getCircum(region:Set[Tuple[int, int]]) -> int:
    ''' Get the circumference for a given region '''

    # Get number of open sides for each coord in region, add those to output
    circum = 0
    for coord in region:
        circum += len(Coord(*coord).getOpenSides(region))
    
    return circum

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Initialization
    out = 0
    visited = set()
    regionList = []
    grid = Grid(inputs)

    # Run BFS to get a list of sets where each set is a region
    for r in range(grid.M):
        for c in range(grid.N):
            if (r,c) not in visited:
                regionSet = bfs(Coord(r,c), grid, visited)
                regionList.append(regionSet)

    # Now get the circumference, area, and output value for each region
    out = 0
    for region in regionList:
        circum = getCircum(region)
        area = len(region)
        out += circum * area

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def toThreeTuple(coord:Coord, cardinal:str) -> Tuple[int, int, int]:
    ''' Given a Coord object and a cardinal direction, return unique 3-tuple '''
    return coord.toTuple() + (cardinal,)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getCircum2(region:Set[Tuple[int, int]]) -> int:
    ''' Get circumference (i.e., number of unique sides) for region in part 2 '''

    # Initialization
    circum = 0
    visited = set()
    CHECK_MAP = {
        'N': ('W', 'E'),
        'S': ('W', 'E'),
        'E': ('N', 'S'),
        'W': ('N', 'S')
    }

    # Iterate through each coordinate in the region
    for coord in region:
        coord = Coord(*coord)

        # Need to check each open side direction for current coordinate
        open_sides = coord.getOpenSides(region)
        for cardinal in open_sides:

            # Now we should check directions perpendicular to cardinal direction
            # Ex: If 'N' is our open side, then we need to check to the 'W' and 'E'
            checkDirs = CHECK_MAP[cardinal]

            # ^^ Using previous example, if the 'N' sides of both our neighbor to the 'W'
            # and neighbor to the 'E' haven't been visited yet, this is a new side          
            if (toThreeTuple(coord.getNeigh(checkDirs[0]), cardinal) not in visited and 
                toThreeTuple(coord.getNeigh(checkDirs[1]), cardinal) not in visited):

                circum += 1

            # Now add our (coordinate + cardinal direction) three-tuple to visited set
            visited.add(toThreeTuple(coord, cardinal))
            
            # ^^ Using previous example, now we need to keep moving westward and adding
            # the 'N' sides of those coordinates to visited as long as they're valid 
            # neighbors with open sides
            coordDir1 = coord.getNeigh(checkDirs[0])
            while (coordDir1.toTuple() in region and 
                   cardinal in coordDir1.getOpenSides(region)):
                visited.add(toThreeTuple(coordDir1, cardinal))
                coordDir1 = coordDir1.getNeigh(checkDirs[0])

            # ^^ Using previous example, we need to also check all the options eastward
            # while valid neighbors with open 'N' sides
            coordDir2 = coord.getNeigh(checkDirs[1])
            while (coordDir2.toTuple() in region and 
                   cardinal in coordDir2.getOpenSides(region)):
                visited.add(toThreeTuple(coordDir2, cardinal))
                coordDir2 = coordDir2.getNeigh(checkDirs[1])
                
    return circum

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Initialization
    out = 0
    visited = set()
    regionList = []
    grid = Grid(inputs)

    # Run BFS to get a list of sets where each set is a region
    for r in range(grid.M):
        for c in range(grid.N):
            if (r,c) not in visited:
                regionSet = bfs(Coord(r,c), grid, visited)
                regionList.append(regionSet)

    # Now get the circumference (num sides), area, and output value for each region
    out = 0
    for region in regionList:
        circum = getCircum2(region)
        area = len(region)
        out += circum * area

    return out

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
