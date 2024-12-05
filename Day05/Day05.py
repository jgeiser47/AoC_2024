'''
    What: Advent of Code 2024 - Day 05
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
class InputsObj():
    ''' Helper object defining our inputs '''
    def __init__(self, rules:map, updates:List[List[int]]):
        self.rules = rules
        self.updates = updates

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def parseInputs(inputs) -> InputsObj:
    ''' do some initial pre-processing of our inputs'''

    # Iterate through the first section of our inputs
    rules = {}
    indSecond = 0
    for ind, input in enumerate(inputs):
        
        # If we've reached an empty line, break this loop and mark that spot
        if len(input) == 0:
            indSecond = ind + 1
            break

        # Otherwise populate our hashmap
        x,y = [int(val) for val in input.split('|')]
        if x in rules:
            rules[x].add(y)
        else:
            rules[x] = {y}

    # Now pre-process the second half of our inputs
    updates = []
    for input in inputs[indSecond:]:
        updates.append([int(val) for val in input.split(',')])

    return InputsObj(rules, updates)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def rulesHold(rules, update):
    ''' For a given "update", check if it abides by our mapping of rules '''

    for x in range(len(update)-1):
        for y in range(x+1, len(update)):
            if ((update[x] in rules and update[y] not in rules[update[x]]) or 
                (update[y] in rules and update[x] in rules[update[y]])):
                return False
            
    return True

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    ''' Solve part 1 '''

    # Initialization
    out = 0
    inputsObj = parseInputs(inputs)

    # For each update that abides by our rules, add its middle number to output 
    for update in inputsObj.updates:
        if rulesHold(inputsObj.rules, update):
            out += update[int(len(update)/2)]
    
    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getFixedUpdate(rules, update):
    ''' Given a non-rule-abiding update, sort it in proper order to follow rules '''

    # Iterate through each value in our original update...
    newUpdate = []
    for val in update:

        # For each value, try putting it in each index of our array until it 
        # passes the rule check
        for i in range(len(newUpdate)+1):
            if rulesHold(rules, newUpdate[:i] + [val] + newUpdate[i:]):
                newUpdate.insert(i, val)
                break
    
    return newUpdate

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    ''' Solve part 2 '''

    # Initialization
    out = 0
    inputsObj = parseInputs(inputs)

    # For each update that DOES NOT abide by our rules, fix it and add middle number
    for update in inputsObj.updates:
        if not rulesHold(inputsObj.rules, update):
            fixedUpdate = getFixedUpdate(inputsObj.rules, update)
            out += fixedUpdate[int(len(fixedUpdate)/2)]

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
