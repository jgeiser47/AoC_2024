'''
    What: Advent of Code 2024 - Day 09
    Who: Josh Geiser
'''

from pathlib import Path
from collections import deque
from typing import List

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def ind2id(ind):
    return int(ind / 2) if ind % 2 == 0 else -1

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Initialization
    inputs = inputs[0]
    IDs = deque()

    # First let's make a stack of all the IDs (with # of occurences)
    for i in range(0, len(inputs), 2):
        for numTimes in range(int(inputs[i])):
            IDs.append(ind2id(i))

    # Initialize other things
    numIDs = len(IDs)
    position = 0
    out = 0

    # For each index in our input string
    for i in range(len(inputs)):

        # If we're on a file space...
        if i % 2 == 0:
            for numTimes in range(int(inputs[i])):

                # ID number is simply based on the index we're at
                out += position * ind2id(i)
                position += 1

                # If our position is ever at total number of IDs, return 
                if position == numIDs:
                    return out
                
        # If we're on a free space
        else:
            for numTimes in range(int(inputs[i])):

                # Pop from our stack
                out += position * IDs.pop()
                position += 1

                # If our position is ever at total number of IDs, return 
                if position == numIDs:
                    return out

    raise SystemError()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class File():
    ''' Class representing a file object that fills space and has an id value '''
    def __init__(self, id, blockStart, size):
        self.id = id
        self.blockStart = blockStart
        self.size = size

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Empty():
    ''' Class representing a block of currently empty space '''
    def __init__(self, blockStart, size):
        self.blockStart = blockStart
        self.size = size

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def findMove(file:File, empties:List[Empty]) -> int:
    ''' For a given file, figure out where (if anywhere) we can move it'''

    # Only need to check for "empty" values to the left of where we currently are
    emptiesInd = 0
    while emptiesInd < len(empties) and empties[emptiesInd].blockStart < file.blockStart:

        # If we've found a viable empty position, return the index in empties array
        if empties[emptiesInd].size >= file.size:
            return emptiesInd

        emptiesInd += 1

    # If the file cannot be moved leftward, return -1
    return -1

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def doMove(file:File, empties:List[Empty], emptiesInd:int):
    ''' For a given file to be moved leftward, actually perform the move '''

    # Block index we're actually moving our file to
    moveIndex = empties[emptiesInd].blockStart

    # Update our current file location
    file.blockStart = moveIndex

    # Now update this "empty" instance since we've placed a block there
    if empties[emptiesInd].size == file.size:
        del empties[emptiesInd]
    else:
        empties[emptiesInd].size -= file.size
        empties[emptiesInd].blockStart += file.size

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getCheckSum(file:File) -> int:
    ''' Return the checksum value for a single file '''
    return sum([file.id * elem for elem in range(file.blockStart, file.blockStart+file.size)])

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Initialization
    inputs = inputs[0]

    # Get a hashmap of string index -> starting block position
    ind2block = {0: 0}
    for i in range(1, len(inputs)):
        ind2block[i] = ind2block[i-1] + int(inputs[i-1])

    # First, let's make a list of all the files
    filesList = []
    for i in range(len(inputs)-1, -1, -2):
        if int(inputs[i]) != 0:
            filesList.append(File(ind2id(i), ind2block[i], int(inputs[i])))

    # Now, let's make a list of all of our empty blocks
    empties = []
    for i in range(1, len(inputs), 2):
        if int(inputs[i]) != 0:
            empties.append(Empty(ind2block[i], int(inputs[i])))

    # Now iterate through each file, attempting to move it leftward and updating checksum
    out = 0
    for file in filesList:

        # If we can move our file leftward, do it
        emptiesInd = findMove(file, empties)
        if emptiesInd != -1:
            doMove(file, empties, emptiesInd)

        # Regardless if moved or not, add the file's checksum to our total
        out += getCheckSum(file)

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
