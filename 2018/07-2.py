import argparse
import re
import string


class Step:

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.workDone = 0
        self.after = []
        self.before = []

    def getName(self):
        return self.name

    def getDuration(self):
        return self.duration

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

    def doWork(self):
        self.workDone += 1

    def __str__(self):
        afterNames = []
        for step in self.after:
            afterNames.append(step.getName())
        beforeNames = []
        for step in self.before:
            beforeNames.append(step.getName())
        return '{0} dur {1}, work done {2}, after {3}, before {4}'.format(
            self.name, self.duration, self.workDone, afterNames, beforeNames)


class Elf:
    def __init__(self, name):
        self.name = name
        self.task = None

    def isOccupied(self):
        return self.task is not None

    def assignTask(self, task):
        self.task = task

    def getTask(self):
        return self.task

    def finishTask(self):
        self.task = None

    def doWork(self):
        self.task.doWork()


def main():
    # Load the sequence
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()

    lines = []
    with open(args.infile) as infile:
        for line in infile:
            lines.append(line.strip())

    # lines = [
    #     'Step C must be finished before step A can begin.',
    #     'Step C must be finished before step F can begin.',
    #     'Step A must be finished before step B can begin.',
    #     'Step A must be finished before step D can begin.',
    #     'Step B must be finished before step E can begin.',
    #     'Step D must be finished before step E can begin.',
    #     'Step F must be finished before step E can begin.'
    # ]

    durations = {}
    i = 1
    for letter in string.ascii_uppercase:
        durations[letter] = 60 + i
        i += 1
    steps = {}

    for line in lines:
        match = re.search(r'Step (.) must be finished before step (.) can begin.', line)
        step1Name = match.group(1)
        step2Name = match.group(2)
        if step1Name not in steps.keys():
            steps[step1Name] = Step(step1Name, durations[step1Name])
        if step2Name not in steps.keys():
            steps[step2Name] = Step(step2Name, durations[step2Name])
        step1 = steps[step1Name]
        step2 = steps[step2Name]
        step1.addBefore(step2)
        step2.addAfter(step1)

    numSteps = len(steps)
    for step in steps.values():
        print(step)
    print()

    workers = [
        Elf('Elf 1'),
        Elf('Elf 2'),
        Elf('Elf 3'),
        Elf('Elf 4'),
        Elf('Elf 5')
    ]

    done = []
    second = 0

    while len(done) < numSteps:
        print('{:3}: '.format(second), end='')
        for elf in workers:
            if not elf.isOccupied():
                availableSteps = []
                for name, step in steps.items():
                    if not step.hasAfter():
                        availableSteps.append(name)
                availableSteps.sort()
                if len(availableSteps) > 0:
                    nextStepName = availableSteps[0]
                    step = steps.pop(nextStepName)
                    elf.assignTask(step)

        for elf in workers:
            if elf.isOccupied():
                elf.doWork()
                step = elf.getTask()
                print('{:2} '.format(step.getName()), end='')
                if step.workDone == step.getDuration():
                    step.done()
                    done.append(step)
                    elf.finishTask()
            else:
                print('{:2} '.format('.'), end='')

        print()
        second += 1

    print()
    print('Order: ', end='')
    for step in done:
        print('{0}'.format(step.getName()), end='')
    print()
    print('Seconds: {0}'.format(second))
    print('Finish')


if __name__ == "__main__":
    main()
