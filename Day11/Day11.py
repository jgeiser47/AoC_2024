'''
    What: Advent of Code 2024 - Day 11
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
def transform(val:int) -> List[int]:
    ''' Our rules for transforming a stone per the instructions'''

    if val == 0:
        return [1]
    elif len(str(val)) % 2 == 0:
        mid = int(len(str(val)) / 2)
        return [int(str(val)[:mid]), int(str(val)[mid:])]
    else:
        return [val * 2024]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Get a list of our inputs
    vals = [int(x) for x in inputs[0].split(' ')]   

    # Now just simulate 25 times, making a new array each time!
    NUM_ITERS = 25  
    for _ in range(NUM_ITERS):
        newVals = []
        for val in vals:
            newVals += transform(val)
        vals = newVals

    return len(vals)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # This time around, let's use a hashmap instead of an array (since the ordering
    # of stones does not matter, only the number of occurences (i.e., frequency) of each)
    hashmap = {}
    inVals = [int(x) for x in inputs[0].split(' ')]   
    for inVal in inVals:
        hashmap[inVal] = 1

    # Now simulate 75 times!
    NUM_ITERS = 75  
    for _ in range(NUM_ITERS):

        # Create a new hashmap for each iteration
        newHashmap = {}

        # Each value from our original hashmap will be transformed,  
        # and then added to our newHashmap (freq) number of times.
        # Ex: if we have 100 "25" stones and 50 "26" stones in hashmap 
        #  -> newHashmap will get 150 "2" stones, 100 "5" stones, and 50 "6" stones
        for val,freq in hashmap.items():
            newVals = transform(val)
            for newVal in newVals:
                if newVal in newHashmap:
                    newHashmap[newVal] += freq 
                else:
                    newHashmap[newVal] = freq
        
        # Now replace our existing hashmap with our newly crafted one
        hashmap = newHashmap
    
    # The sum of all the values in the hashmap is the total number of stones
    return sum(hashmap.values())

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
