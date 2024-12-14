'''
    What: Advent of Code 2024 - Day 13
    Who: Josh Geiser
'''

from pathlib import Path
from typing import List
import re

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Game():
    ''' Helper class for defining a single instance of a game '''
    def __init__(self, chunk:List[str], part2:bool=False):
        conversion = 10000000000000 if part2 else 0
        self.A = tuple([int(x[1:]) for x in re.findall('\+\d+', chunk[0])])
        self.B = tuple([int(x[1:]) for x in re.findall('\+\d+', chunk[1])])
        self.Prize = tuple([int(x[1:])+conversion for x in re.findall('\=\d+', chunk[2])])

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def parseInputs(inputs:List[str], part2:bool=False) -> List[Game]:
    ''' Populate our inputs into a list of games '''

    games = []
    for i in range(0, len(inputs), 4):
        games.append(Game(inputs[i:i+4], part2))

    return games

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def numTokens(numA:int, numB:int) -> int:
    ''' Given number of pushes of each A and B, return cost '''
    return (3 * numA) + numB

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def runGame(game:Game) -> int:
    ''' Return cost if game is winable, otherwise return -1 if not '''

    # Iterate up to 100 times
    for numA in range(0, 101):

        # Calculate the reaminign difference for a given number of A presses
        diffA = (numA * game.A[0], numA * game.A[1])
        remaining = (game.Prize[0] - diffA[0], game.Prize[1] - diffA[1])

        # See if an integer number of B presses fits this criteria
        if (remaining[0] % game.B[0] == 0 and 
            remaining[1] % game.B[1] == 0 and
            int(remaining[0] / game.B[0]) == int(remaining[1] / game.B[1])):

            # If so, can return now
            numB = int(remaining[0] / game.B[0])
            return numTokens(numA, numB)
        
        # Prune cases if we're past our goal 
        if (remaining[0] < 0 or remaining[1] < 0):
            return -1

    # Cannot win
    return -1

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Define things
    out = 0
    games = parseInputs(inputs)

    # Do the thing
    for game in games:
        gameVal = runGame(game)
        if gameVal > 0:
            out += gameVal

    return out 

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def runGame2(game:Game) -> int:
    '''
        Here's some ASCII text of my pen & paper math: 

        A * C_00 + B * C_10 = C_20
        A * C_01 + B * C_11 = C_21

        -> B = (C_21 - (A * C_01)) / C_11
        -> A * C_00 + (C_10/C_11) * (C_21 - (A * C_01)) = C_20
        -> A * C_00 + (C_10*C_21/C_11) - A * (C_01*C_10/C_11) = C_20
        -> A = [C_20 - (C_10*C_21/C_11)] / [C_00 - (C_01*C_10/C_11)]
    
    '''

    # I don't like how sensitive the final answer is to our precision tolerance
    TOL = 1e-3

    # Rename our constant terms
    C_00 = game.A[0]
    C_01 = game.A[1]
    C_10 = game.B[0]
    C_11 = game.B[1]
    C_20 = game.Prize[0]
    C_21 = game.Prize[1]

    # If number of A presses is an integer (within some tolerance)
    numA = (C_20 - (C_10*C_21/C_11)) / (C_00 - (C_01*C_10/C_11))
    if abs(round(numA) - numA) > TOL:
        return -1
    
    # Now calculate what B should be 
    numArounded = round(numA)
    numB = (C_21 - (numArounded * C_01)) / C_11

    # Same deal: make sure number of B presses is an integer (within tolerance)
    if abs(round(numB) - numB) > TOL:
        return -1
    
    # If we've gotten this far, then yay return cost
    numBrounded = round(numB)
    return numTokens(numArounded, numBrounded)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Define things
    out = 0
    games = parseInputs(inputs, part2=True)

    # Do the thing
    for game in games:
        gameVal = runGame2(game)
        if gameVal > 0:
            out += gameVal

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
