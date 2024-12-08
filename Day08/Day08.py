'''
    What: Advent of Code 2024 - Day 08
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

    def __contains__(self, coord:Coord) -> bool:
        ''' So that we can do things like: if coord in grid '''
        return 0 <= coord.r < self.M and 0 <= coord.c < self.N
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def parseInputs(grid:Grid):
    ''' Get a hashmap mapping a letter to a list of coordinates of that letter '''

    hashmap = {}
    for r in range(grid.M):
        for c in range(grid.N):
            if grid.grid[r][c] == '.':
                continue
            elif grid.grid[r][c] in hashmap:
                hashmap[grid.grid[r][c]].append(Coord(r,c))
            else:
                hashmap[grid.grid[r][c]] = [Coord(r,c)]

    # hashmap = map[str, List[Coord]]
    return hashmap

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def findAntinodes(coord1:Coord, coord2:Coord, grid:Grid, antinodeLocs:set):
    ''' Given two specific coordinates of same letter, find their antinodes '''

    # Relative offset between coordinates
    dr, dc = coord2.r-coord1.r, coord2.c-coord1.c

    # Possible antinode locations
    possibleAntinode1 = Coord(coord1.r-dr, coord1.c-dc)
    possibleAntinode2 = Coord(coord2.r+dr, coord2.c+dc)

    # If possible antinode coordinate is in grid, add it to our output set
    if possibleAntinode1 in grid:
        antinodeLocs.add(str(possibleAntinode1))

    # If possible antinode coordinate is in grid, add it to our output set
    if possibleAntinode2 in grid:
        antinodeLocs.add(str(possibleAntinode2))

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Initialize things
    grid = Grid(inputs)
    hashmap = parseInputs(grid)
    antinodeLocs = set()

    # For each unique letter
    for letterCoords in hashmap.values():

        # Don't do anything if there's only one instance of this letter
        if len(letterCoords) < 2:
            break

        # For every combo of letterCoords for a given letter
        for i in range(len(letterCoords)-1):
            for j in range(i+1, len(letterCoords)):
                findAntinodes(letterCoords[i], letterCoords[j], grid, antinodeLocs)

    # Output is just the number of unique antinode locations
    return len(antinodeLocs)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def findAntinodes2(coord1:Coord, coord2:Coord, grid:Grid, antinodeLocs:set):

    # Relative offset between coordinates
    dr, dc = coord2.r-coord1.r, coord2.c-coord1.c

    # Possible antinode coordinate in one direction
    while coord1 in grid:
        antinodeLocs.add(str(coord1))
        coord1 = Coord(coord1.r-dr, coord1.c-dc)

    # Possible antinode coordinate in the other direction
    while coord2 in grid:
        antinodeLocs.add(str(coord2))
        coord2 = Coord(coord2.r+dr, coord2.c+dc)

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Initialize things
    grid = Grid(inputs)
    hashmap = parseInputs(grid)
    antinodeLocs = set()

    # For each unique letter
    for letterCoords in hashmap.values():

        # Don't do anything if there's only one instance of this letter
        if len(letterCoords) < 2:
            break

        # For every combo of letterCoords for a given letter
        for i in range(len(letterCoords)-1):
            for j in range(i+1, len(letterCoords)):
                findAntinodes2(letterCoords[i], letterCoords[j], grid, antinodeLocs)

    # Output is just the number of unique antinode locations
    return len(antinodeLocs)
    
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
