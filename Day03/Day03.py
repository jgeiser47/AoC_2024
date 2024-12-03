'''
    What: Advent of Code 2024 - Day 03
    Who: Josh Geiser
'''

from pathlib import Path
import re

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def expr2val(match:str) -> int:
    ''' If we have a match string like "mul(x,y)", return the value of x * y '''
    return int(match.split('(')[1].split(',')[0]) * int(match.split(',')[1].split(')')[0])

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    '''
        Regular expressions ftw! Thanks to references like:
        https://www.geeksforgeeks.org/python-regex-cheat-sheet/
    '''
    out = 0
    pattern = 'mul\(\d+,\d+\)'
    for input in inputs:
        matches = re.findall(pattern, input)
        for match in matches:
            out += expr2val(match)

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Now match anything like "mul(x,y)", "don't()", or "do()"
    total_matches = []
    pattern = "mul\(\d+,\d+\)|do\(\)|don't\(\)"
    for input in inputs:
        matches = re.findall(pattern, input)
        total_matches += matches
        
    # Only add our match if we are currently in a "do()" state
    out = 0
    iDo = True
    for match in total_matches:
        if 'mul' in match and iDo:
            out += expr2val(match)
        elif match == "don't()":
            iDo = False
        elif match == "do()":
            iDo = True

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
