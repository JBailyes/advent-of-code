import argparse
import os
import re

from aocutils import load_input


def main():
    # puzzle_input = load_input(__file__)
    puzzle_input = load_input(__file__, 'example')

    starting_numbers = [int(n) for n in puzzle_input[0].split(',')]

    history = {}
    turn = 1
    for number in starting_numbers:
        history[number] = [turn]
        turn += 1

    last_number = starting_numbers[-1]
    while turn < 10:
        if history[last_number].count(last_number) == 1:
            new_number = 0
        else:
            new_number = history[last_number][-1] - history[last_number][-2]

        if new_number not in history.keys():
            history[new_number] = []
        history[new_number].append(turn)
        last_number = new_number

        print(last_number)
        turn += 1

    print(last_number)


if __name__ == "__main__":
    main()
