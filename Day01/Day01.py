'''
    What: Advent of Code 2024 - Day 01
    Who: Josh Geiser
'''

from pathlib import Path
from queue import Queue
import math

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Split numbers into left and right arrays
    left, right  = [], []
    for input in inputs:
        numList = input.strip().split()
        left.append(int(numList[0]))
        right.append(int(numList[-1]))

    # Now sort our lists
    left.sort()
    right.sort()

    # Now we can sum up the differences in our lists
    out = 0
    for i in range(len(left)):
        out += abs(left[i] - right[i])
    
    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Split numbers into left and right arrays
    left, right  = [], []
    for input in inputs:
        numList = input.strip().split()
        left.append(int(numList[0]))
        right.append(int(numList[-1]))

    # List.count() method comes very much in handy here
    out = 0
    for num in left:
        out += num * right.count(num)
    
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
