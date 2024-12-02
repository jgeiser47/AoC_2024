'''
    What: Advent of Code 2024 - Day 02
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
def isLineSafe(line):
    
    # Get our differences between each value
    diff = []
    for i in range(len(line)-1):
        diff.append(line[i+1] - line[i])

    # If they're either all ascending/descending in the appropriate range, then true
    return all([1 <= x <= 3 for x in diff]) or all([-3 <= x <= -1 for x in diff])

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Do the thing
    out = 0
    for input in inputs:
        line = [int(x) for x in input.strip().split(' ')]
        if isLineSafe(line):
            out += 1

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def partTwoIsSafe(line):

    # Prune off any cases with multiple instances of repeat values
    if abs(len(set(line)) - len(line)) > 1:
        return False

    # Get our differences between each value
    diff = []
    for i in range(len(line)-1):
        diff.append(line[i+1] - line[i])

    # If all of our differences are in the appropriate range, then already safe
    if all([1 <= x <= 3 for x in diff]) or all([-3 <= x <= -1 for x in diff]):
        return True

    # Otherwise, lets just brute force removing a single value at a time and
    # see if any of those combinations are safe
    for i in range(len(line)):
        if isLineSafe(line[:i] + line[i+1:]):
            return True

    # If nothing is safe at this point, return false
    return False

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Do the thing, but part 2
    out = 0
    for input in inputs:
        line = [int(x) for x in input.strip().split(' ')]
        if partTwoIsSafe(line):
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
