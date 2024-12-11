'''
    What: Advent of Code 2024 - Day 10
    Who: Josh Geiser
'''

from pathlib import Path

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

    def __str__(self):
        return f'{self.r}_{self.c}'
    
    def toTuple(self):
        return (self.r, self.c)
    
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
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getNeighs(coord:Coord, grid:Grid):
    ''' Get the neighbors for a given coordinate '''

    # Look in each of 4 potential directions
    DIRS = [(+1, +0), (-1, +0), (+0, -1), (+0, +1)]
    out = []
    for dr, dc in DIRS:
        neigh = Coord(coord.r+dr, coord.c+dc)

        # Each valid neighbor should be in grid and have a value of 1 greater than current
        if (neigh in grid and
            int(grid.grid[coord.r][coord.c]) + 1 == int(grid.grid[neigh.r][neigh.c])):
            out.append(neigh)

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getNeighsMap(grid:Grid):
    ''' Get a hashmap of each coordinate's neighbors: (r,c) -> List[Coord] '''

    neighs = {}
    for r in range(grid.M):
        for c in range(grid.N):
            neighs[(r,c)] = getNeighs(Coord(r,c), grid)

    return neighs

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getScore(coord:Coord, grid:Grid, neighs:dict, scoreCoords):
    ''' Recursive function to get the "score" of a given trailhead '''

    # Base case - we've reached a 9
    if grid.grid[coord.r][coord.c] == '9':
        scoreCoords.add(coord.toTuple())
        return
    
    # Recursive case - make recursive call with each of our neighbors
    for neighCoord in neighs[coord.toTuple()]:
        getScore(neighCoord, grid, neighs, scoreCoords)

    return 

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Initialize
    grid = Grid(inputs)
    neighs = getNeighsMap(grid)
    out = 0

    # For each trailhead, get its score!
    for r in range(grid.M):
        for c in range(grid.N):
            if grid.grid[r][c] == '0':
                scoreCoords = set()
                getScore(Coord(r,c), grid, neighs, scoreCoords)
                out += len(scoreCoords)

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getScore2(coord:Coord, grid:Grid, neighs:dict):
    ''' Recursive function to get the "score" of a given trailhead '''

    # Base case - we've reached a 9
    if grid.grid[coord.r][coord.c] == '9':
        return 1
    
    # Recursive case - make recursive call with each of our neighbors
    out = 0
    for neighCoord in neighs[coord.toTuple()]:
        out += getScore2(neighCoord, grid, neighs)

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Initialize
    grid = Grid(inputs)
    neighs = getNeighsMap(grid)
    out = 0

    # For each trailhead, get its score!
    for r in range(grid.M):
        for c in range(grid.N):
            if grid.grid[r][c] == '0':
                out += getScore2(Coord(r,c), grid, neighs)

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
