import argparse
import re
import string
from datetime import datetime


class Pots:
    def __init__(self, state):
        self.pots = {}
        self.nextGen = {}
        print('parse state: ' + state)
        number = 0
        for plant in state:
            self.pots[number] = plant
            number += 1
        for n in range(-5, 0):
            self.pots[n] = '.'
        for n in range(number, number + 5):
            self.pots[n] = '.'
        self.__calculateBounds()

    def __calculateBounds(self):
        self.leftmost = None
        self.rightmost = None
        numbers = sorted(self.pots.keys())
        n = numbers[0]
        while self.leftmost is None:
            if self.pots[n] == '#':
                self.leftmost = n
            n += 1
        n = numbers[-1]
        while self.rightmost is None:
            if self.pots[n] == '#':
                self.rightmost = n
            n -= 1

    def getPot(self, number):
        return self.pots[number]

    def leftmostPlant(self):
        return self.leftmost

    def rightmostPlant(self):
        return self.rightmost

    def leftmostPot(self):
        return sorted(self.pots.keys())[0]

    def rightmostPot(self):
        return sorted(self.pots.keys())[-1]

    def setPotForNextGen(self, number, plant):
        self.nextGen[number] = plant

    def getSurrounding(self, number):
        surrounding = ''
        for n in range(number - 2, number + 3):
            if n in self.pots.keys():
                surrounding += self.pots[n]
            else:
                surrounding += '.'
        return surrounding

    def nextGeneration(self):
        self.pots = self.nextGen
        self.nextGen = {}
        self.__calculateBounds()
        for n in range(self.leftmost - 5, self.leftmost):
            self.pots[n] = '.'
        for n in range(self.rightmost + 1, self.rightmost + 5):
            self.pots[n] = '.'

    def getPots(self):
        return self.pots

    def sumPlants(self):
        total = 0
        for number, plant in self.pots.items():
            if plant == '#':
                total += number
        return total

    def __str__(self):
        state = ''
        for number in sorted(self.pots.keys()):
            state += self.pots[number]
        return state


class Rule:
    def __init__(self, fullRule):
        self.rule = fullRule[0:5]
        self.outcome = fullRule[9]

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
            pots = Pots(line.split(' ')[2])
            print('Initial state: {0}'.format(pots))
        else:
            rules.append(Rule(line))

    for potNum in range(0, len(rules)):
        print('Rule {0:2}: {1}'.format(potNum + 1, rules[potNum]))

    genlines = [pots.getPots()]
    minPot = 0
    maxPot = 0

    start = datetime.now()
    for generation in range(1, int(args.generations) + 1):
        if generation % 500 == 0:
            print('G {0}'.format(generation))
        for potNum in range(pots.leftmostPot(), pots.rightmostPot() + 1):
            ruleMatched = False
            for rule in rules:
                if rule.apply(pots, potNum):
                    ruleMatched = True
            if not ruleMatched:
                pots.setPotForNextGen(potNum, '.')
        pots.nextGeneration()
        genlines.append(pots.getPots())
        minPot = min(minPot, pots.leftmostPot())
        maxPot = max(maxPot, pots.rightmostPot())
    end = datetime.now()

    # for genNum, genLine in enumerate(genlines):
        # print('G{0:2}: '.format(genNum), end='')
        # for potNum in range(minPot, maxPot + 1):
            # if potNum in genLine.keys():
            #     print('{0}'.format(genLine[potNum]), end='')
            # else:
            #     print(' ', end='')
        # print()

    print('Duration: {0}'.format(end - start))
    print()
    print('Sum of pots containing plants: {0:,}'.format(pots.sumPlants()))

    print()
    print('Finish')


if __name__ == "__main__":
    main()
