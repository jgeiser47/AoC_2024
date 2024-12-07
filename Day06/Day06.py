'''
    What: Advent of Code 2024 - Day 06
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

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Grid():
    ''' Helper class for storing properties of our grid '''

    def __init__(self, grid):
        self.grid = grid
        self.M = len(grid)
        self.N = len(grid[0])
        self.startPos = None

    def __contains__(self, coord:Coord) -> bool:
        ''' So that we can do things like: if coord in grid '''
        return 0 <= coord.r < self.M and 0 <= coord.c < self.N
    
    def updateInd(self, r, c, char):
        ''' Since strings are immutable, have to do some hackier logic '''
        row = self.grid[r]
        self.grid[r] = row[:c] + char + row[c+1:]
        return
        
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Direction():
    ''' Helper class for what "direction" we are facing '''

    def __init__(self, startDir='UP'):
        self.DIRS = ['UP', 'RIGHT', 'DOWN', 'LEFT']
        self.STEP_TO_TAKE = {
            'UP':       (-1, +0),
            'RIGHT':    (+0, +1),
            'DOWN':     (+1, +0),
            'LEFT':     (+0, -1)
        }
        self.facing = startDir

    def __str__(self):
        return self.facing

    def updateDir(self):
        ''' Go from UP -> RIGHT -> DOWN -> LEFT '''
        self.facing = self.DIRS[(self.DIRS.index(self.facing) + 1) % len(self.DIRS)]

    def getStep(self, coord:Coord) -> Coord:
        ''' Given our current direction and coord, give next potential coord '''
        dr, dc = self.STEP_TO_TAKE[self.facing]
        return Coord(coord.r + dr, coord.c + dc)

    def takeStep(self, coord:Coord, grid:Grid) -> Coord:
        ''' Decide where to take our next step '''

        newCoord = self.getStep(coord)

        # If we're out of bounds, that's ok, we're at the end!
        if newCoord not in grid:
            return newCoord
        
        # This bug/edge case took me forever to figure out :/ 
        # have to do a while loop instead of an if for cases like this: 
        #       .#
        #       #<
        while grid.grid[newCoord.r][newCoord.c] == '#':
            self.updateDir()
            newCoord = self.getStep(coord)

        return newCoord
        
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getStart(grid:Grid) -> Coord:
    ''' Figure out where our starting position is. Also update grid with that info '''
    for r in range(grid.M):
        for c in range(grid.N):
            if grid.grid[r][c] == '^':
                grid.startPos = Coord(r, c) # bad side effect
                return grid.startPos
    raise SystemExit()
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Initialize things
    grid = Grid(inputs)
    visited = set()
    currDir = Direction()
    curr = getStart(grid)

    # Iterate 'til we done
    while curr in grid:
        visited.add(str(curr))
        curr = currDir.takeStep(curr, grid)

    # Length of our hashset is simply our answer
    return len(visited)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def toSet(coord:Coord, direction:Direction) -> str:
    ''' For adding unique coord/direction entries into our hashset '''
    return str(coord) + '_' + str(direction)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def testIfLoop(blockerCoord:Coord, testDir:Direction, testGrid:Grid):

    # We can't add a blocker to the start coordinate, so return immediately
    if blockerCoord.r == testGrid.startPos.r and blockerCoord.c == testGrid.startPos.c:
        return 0

    # Add in our new blocker "#"
    origVal = testGrid.grid[blockerCoord.r][blockerCoord.c]
    testGrid.updateInd(blockerCoord.r, blockerCoord.c, '#')

    # Initialize things
    visited = set()
    testCoord = Coord(testGrid.startPos.r, testGrid.startPos.c)

    # Now iterate until either we're out of the grid or we've reached a loop
    while testCoord in testGrid and toSet(testCoord, testDir) not in visited:
        visited.add(toSet(testCoord, testDir))
        testCoord = testDir.takeStep(testCoord, testGrid)

    # Have to be sure to revert our grid back since we're passing by reference
    testGrid.updateInd(blockerCoord.r, blockerCoord.c, origVal)

    # If we're still in the grid, then hoorah this blocker caused a loop!
    return 1 if testCoord in testGrid else 0

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Initialize things
    out = 0
    grid = Grid(inputs)
    currDir = Direction()
    actualVisited = set()
    curr = getStart(grid)

    # Basically redo part 1 so we have a hashset of all our visited coords
    while curr in grid:
        actualVisited.add(str(curr))
        curr = currDir.takeStep(curr, grid)

    # Now for each of those visited coords, try putting a blocker and see if
    # that causes us to be in an infinite loop
    for curr in actualVisited:
        blockerCoord = Coord(*[int(x) for x in curr.split('_')])
        out += testIfLoop(blockerCoord, Direction(), grid)

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
