import argparse
import re
import string
from datetime import datetime


class Pots:
    def __init__(self):
        self.pots = {}
        self.nextGen = None
        self.leftmostPlantNumber = 0
        self.rightmostPlantNumber = 0
        self.leftmostPotNumber = 0
        self.rightmostPotNumber = 0

    def fromState(self, state):
        print('parse state: ' + state)
        self.nextGen = Pots()
        number = 0
        for plant in state:
            if plant == '#':
                self.setPot(number, 1)
            else:
                self.setPot(number, 0)
            number += 1
        for n in range(-5, 0):
            self.setPot(n, 0)
        for n in range(number, number + 5):
            self.setPot(n, 0)

    def getPot(self, number):
        return self.pots[number]

    def leftmostPlant(self):
        return self.leftmostPlantNumber

    def rightmostPlant(self):
        return self.rightmostPlantNumber

    def leftmostPot(self):
        return self.leftmostPotNumber

    def rightmostPot(self):
        return self.rightmostPotNumber

    def setPot(self, number, plant):
        self.pots[number] = plant
        if plant == 1:
            if number < self.leftmostPlantNumber:
                self.leftmostPlantNumber = number
            elif number > self.rightmostPlantNumber:
                self.rightmostPlantNumber = number
        if number < self.leftmostPotNumber:
            self.leftmostPotNumber = number
        elif number > self.rightmostPotNumber:
            self.rightmostPotNumber = number

    def setPotForNextGen(self, number, plant):
        self.nextGen.setPot(number, plant)

    def getSurrounding(self, number):
        surrounding = []
        for n in range(number - 2, number + 3):
            if n in self.pots.keys():
                surrounding.append(self.pots[n])
            else:
                surrounding.append(0)
        return surrounding

    def __addNextGen__(self):
        self.nextGen = Pots()

    def nextGeneration(self):
        for n in range(self.nextGen.leftmostPlant() - 5, self.nextGen.leftmostPlant()):
            self.nextGen.setPot(n, 0)
        for n in range(self.nextGen.rightmostPlant() + 1, self.nextGen.rightmostPlant() + 5):
            self.nextGen.setPot(n, 0)
        self.nextGen.__addNextGen__()
        return self.nextGen

    def getPots(self):
        return self.pots

    def sumPlants(self):
        total = 0
        for number, plant in self.pots.items():
            if plant == 1:
                total += number
        return total

    def __str__(self):
        state = ''
        for number in sorted(self.pots.keys()):
            state += str(self.pots[number])
        return state


class Rule:
    def __init__(self, fullRule):
        self.rule = [0, 0, 0, 0, 0]
        self.outcome = 0
        for i, char in enumerate(fullRule[0:5]):
            if char == '#':
                self.rule[i] = 1
        if fullRule[9] == '#':
            self.outcome = 1

    def apply(self, pots, number):
        if pots.getSurrounding(number) == self.rule:
            pots.setPotForNextGen(number, self.outcome)
            return True
        return False

    def __str__(self):
        return '{0} > {1}'.format(self.rule, self.outcome)


def main():
    # Load the sequence
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('generations')
    args = parser.parse_args()

    lines = []
    with open(args.infile) as infile:
        for line in infile:
            if len(line.strip()) > 0:
                lines.append(line.strip())

    rules = []

    for line in lines:
        if 'initial state' in line:
            pots = Pots()
            pots.fromState(line.split(' ')[2])
            print('Initial state: {0}'.format(pots))
        else:
            rules.append(Rule(line))

    # for potNum in range(0, len(rules)):
    #     print('Rule {0:2}: {1}'.format(potNum + 1, rules[potNum]))

    genTotals = {pots.sumPlants(): 0}
    initialState = str(pots)

    overallStart = datetime.now()
    lastGenStart = overallStart
    lastGenScore = 0

    for generation in range(1, int(args.generations) + 1):
        # if generation % 500 == 0:
        #     timeNow = datetime.now()
        #     print('G {0}, {1}'.format(generation, timeNow - lastGenStart))
        #     lastGenStart = timeNow
        for potNum in range(pots.leftmostPot(), pots.rightmostPot() + 1):
            ruleMatched = False
            for rule in rules:
                if not ruleMatched and rule.apply(pots, potNum):
                    ruleMatched = True
        pots = pots.nextGeneration()
        score = pots.sumPlants()
        diff = score - lastGenScore
        print('G{0:,}: score {1}, diff to last {2}'.format(generation, score, diff))
        lastGenScore = score

        # genline = pots.getPots()
        # if genline in genlines:
        #     print('Repeat at generation {0}: {1}'.format(generation, genline))
        # genlines.append(pots.getPots())
        # minPot = min(minPot, pots.leftmostPot())
        # maxPot = max(maxPot, pots.rightmostPot())
    end = datetime.now()

    # for genNum, genLine in enumerate(genlines):
        # print('G{0:2}: '.format(genNum), end='')
        # for potNum in range(minPot, maxPot + 1):
            # if potNum in genLine.keys():
            #     print('{0}'.format(genLine[potNum]), end='')
            # else:
            #     print(' ', end='')
        # print()

    print('Duration: {0}'.format(end - overallStart))
    print()
    print('Sum of pots containing plants: {0:,}'.format(pots.sumPlants()))
    print('Len: {0}'.format(len(str(pots))))
    print()
    print('Finish')


if __name__ == "__main__":
    main()
