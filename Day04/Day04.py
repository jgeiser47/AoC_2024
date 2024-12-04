'''
    What: Advent of Code 2024 - Day 04
    Who: Josh Geiser
'''

from pathlib import Path
from typing import List

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def coordInGrid(r, c, M, N) -> bool:
    ''' Is our current (row, col) coordinate within our grid '''
    return 0 <= r< M and 0 <= c < N

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def checkDirection(direction, inputs, r, c, M, N) -> bool:
    ''' 
    Given a starting point (r,c) and a direction (e.g., left, up, diag, etc.), is
    this a valid "XMAS" string
    '''

    LETTERS = 'XMAS'

    for i, letter in enumerate(LETTERS):
        if coordInGrid(r, c, M, N) and inputs[r][c] == letter:
            r += direction[0]
            c += direction[1]
        else:
            return False
        
    return True

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Matrix dimension
    M = len(inputs)
    N = len(inputs[0])

    # All possible directions to search
    DIRECTIONS = {
        (-1, 0), (-1, +1), (0, +1), (+1, +1), (+1, 0), (+1, -1), (0, -1), (-1, -1)
    }

    # Check each (row,col) starting point. For each starting point, check each direction
    out = 0
    for r in range(M):
        for c in range(N):
            for direction in DIRECTIONS:
                if checkDirection(direction, inputs, r, c, M, N):
                    out += 1

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def helper(arr:List[str], instr:str) -> str:
    ''' Given a 3x3 subarray, return the character in the specified corner '''
    mapping = {
        'topleft' : arr[0][0],
        'topright': arr[0][2],
        'botleft' : arr[2][0],
        'botright': arr[2][2]
    }
    return mapping[instr]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def isXMas(arr:List[str]) -> bool:
    ''' 
    Ugly helper logic - given a 3x3 subarray, returns True if two adjacent corners
    contain "M" and the other two contain "S", False otherwise
    '''
    return (
        (helper(arr,'topleft') == helper(arr,'topright') == 'M' and
         helper(arr,'botleft') == helper(arr,'botright') == 'S') 
         or
        (helper(arr,'topright') == helper(arr,'botright') == 'M' and
         helper(arr,'topleft') == helper(arr,'botleft') == 'S') 
         or
        (helper(arr,'botleft') == helper(arr,'botright') == 'M' and
         helper(arr,'topleft') == helper(arr,'topright') == 'S') 
         or 
        (helper(arr,'botleft') == helper(arr,'topleft') == 'M' and
         helper(arr,'botright') == helper(arr,'topright') == 'S')
    )

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Matrix dimensions
    M = len(inputs)
    N = len(inputs[0])

    # For each (r,c) coordinate as the center of a 3x3 subarray, check if that
    # subarray fulfills our X-MAS subarray specification
    out = 0
    for r in range(1, M-1):
        for c in range(1, N-1):
            if inputs[r][c] == 'A':
                subarray = [row[c-1:c+2] for row in inputs[r-1:r+2]]
                if isXMas(subarray):
                    out += 1

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
