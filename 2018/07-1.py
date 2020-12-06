import argparse
import re
import string


class Step:

    def __init__(self, name):
        self.name = name
        self.after = []
        self.before = []

    def getName(self):
        return self.name

    def getBefore(self):
        return self.before

    def getAfter(self):
        return self.after

    def addBefore(self, step):
        self.before.append(step)

    def addAfter(self, step):
        self.after.append(step)

    def hasBefore(self):
        return len(self.before) > 0

    def hasAfter(self):
        return len(self.after) > 0

    def done(self):
        for step in self.before:
            step.getAfter().remove(self)

    def __str__(self):
        afterNames = []
        for step in self.after:
            afterNames.append(step.getName())
        beforeNames = []
        for step in self.before:
            beforeNames.append(step.getName())
        return '{0}, after {1}, before {2}'.format(self.name, afterNames, beforeNames)


def main():
    # Load the sequence
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()

    lines = []
    with open(args.infile) as infile:
        for line in infile:
            lines.append(line.strip())
    #
    # lines = [
    #     'Step C must be finished before step A can begin.',
    #     'Step C must be finished before step F can begin.',
    #     'Step A must be finished before step B can begin.',
    #     'Step A must be finished before step D can begin.',
    #     'Step B must be finished before step E can begin.',
    #     'Step D must be finished before step E can begin.',
    #     'Step F must be finished before step E can begin.'
    # ]

    steps = {}

    for line in lines:
        match = re.search(r'Step (.) must be finished before step (.) can begin.', line)
        step1Name = match.group(1)
        step2Name = match.group(2)
        if step1Name not in steps.keys():
            steps[step1Name] = Step(step1Name)
        if step2Name not in steps.keys():
            steps[step2Name] = Step(step2Name)
        step1 = steps[step1Name]
        step2 = steps[step2Name]
        step1.addBefore(step2)
        step2.addAfter(step1)

    # print(steps)
    for step in steps.values():
        print(step)
    print()

    while len(steps) > 0:
        available = []
        for name, step in steps.items():
            if not step.hasAfter():
                available.append(name)
        available.sort()
        nextStepName = available[0]
        step = steps.pop(nextStepName)
        step.done()
        print(step.getName(), end='')

    print()
    print('Finish')


if __name__ == "__main__":
    main()
