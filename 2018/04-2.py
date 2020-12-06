import argparse
import re


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
    #     '[1518-11-01 00:00] Guard #10 begins shift',
    #     '[1518-11-01 00:05] falls asleep',
    #     '[1518-11-01 00:25] wakes up',
    #     '[1518-11-01 00:30] falls asleep',
    #     '[1518-11-01 00:55] wakes up',
    #     '[1518-11-01 23:58] Guard #99 begins shift',
    #     '[1518-11-02 00:40] falls asleep',
    #     '[1518-11-02 00:50] wakes up',
    #     '[1518-11-03 00:05] Guard #10 begins shift',
    #     '[1518-11-03 00:24] falls asleep',
    #     '[1518-11-03 00:29] wakes up',
    #     '[1518-11-04 00:02] Guard #99 begins shift',
    #     '[1518-11-04 00:36] falls asleep',
    #     '[1518-11-04 00:46] wakes up',
    #     '[1518-11-05 00:03] Guard #99 begins shift',
    #     '[1518-11-05 00:45] falls asleep',
    #     '[1518-11-05 00:55] wakes up'
    # ]

    sleeps = {}

    for line in sorted(lines):
        match = re.search(r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\]', line)
        if match:
            minute = int(match.group(5))
            guardMatch = re.search(r'Guard #(\d+)', line)
            if guardMatch:
                guard = guardMatch.group(1)
                if guard not in sleeps.keys():
                    sleeps[guard] = {}.fromkeys(range(0, 60), 0)
            elif 'falls asleep' in line:
                sleepStart = minute
            elif 'wakes up' in line:
                sleepEnd = minute
                for sleepMinute in range(sleepStart, sleepEnd):
                    sleeps[guard][sleepMinute] += 1

    maxMinuteRecurrence = 0
    for guard in sleeps.keys():
        for minute in sleeps[guard].keys():
            if sleeps[guard][minute] > maxMinuteRecurrence:
                maxMinuteRecurrence = sleeps[guard][minute]
                chosenMinute = minute
                chosenGuard = guard

    print('Guard #{0} slept {1} times on minute {2}'.format(chosenGuard, maxMinuteRecurrence, chosenMinute))

    print('Answer: {0} * {1} = {2}'.format(chosenGuard, chosenMinute, int(chosenGuard) * chosenMinute))

    print('Finish')


if __name__ == "__main__":
    main()
