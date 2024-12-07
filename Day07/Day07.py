'''
    What: Advent of Code 2024 - Day 07
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
def parseLine(line:str) -> tuple[int, List[int]]:
    ''' Helper for getting our inputs into the form we need'''
    left, right = line.split(': ')
    return int(left), [int(x) for x in right.split(' ')]
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def recurse(testVal:int, nums:List[int]) -> bool:
    ''' Recursive logic for testing all combinations of "+" and "*" '''

    # Base case: we're left with one number in nums, see if it's equal to testVal
    if len(nums) == 1:
        return testVal == nums[0]
    
    # Prune off any cases that are already larger than testVal
    if nums[0] > testVal:
        return False

    # Recursive case: try "+" and "*"
    case1 = recurse(testVal, [nums[0] + nums[1]] + nums[2:])
    case2 = recurse(testVal, [nums[0] * nums[1]] + nums[2:])

    # Return true if any combination is true
    return case1 or case2 

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # For each line in our file, recursively check all combinations of operations
    out = 0
    for input in inputs:
        testVal, nums = parseLine(input)
        if recurse(testVal, nums):
            out += testVal

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def recurse2(testVal:int, nums:List[int]) -> bool:
    ''' Recursive logic for testing all combinations of "+", "*", and "||" '''

    # Base case: we're left with one number in nums, see if it's equal to testVal
    if len(nums) == 1:
        return testVal == nums[0]
    
    # Prune off any cases that are already larger than testVal
    if nums[0] > testVal:
        return False

    # Recursive case: try "+" and "*" and "||"
    case1 = recurse2(testVal, [nums[0] + nums[1]] + nums[2:])
    case2 = recurse2(testVal, [nums[0] * nums[1]] + nums[2:])
    case3 = recurse2(testVal, [int( str(nums[0]) + str(nums[1]) )] + nums[2:])

    # Return true if any combination is true
    return case1 or case2 or case3

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # For each line in our file, recursively check all combinations of operations
    out = 0
    for input in inputs:
        testVal, nums = parseLine(input)
        if recurse2(testVal, nums):
            out += testVal

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
