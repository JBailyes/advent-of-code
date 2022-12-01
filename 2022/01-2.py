import re

from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    totals = []

    current_total = 0
    for line in puzzle_input + ['']:
        if line == '':
            totals.append(current_total)
            current_total = 0
        else:
            current_total += int(line)
    
    # Correct answer: 205615
    print(sum(sorted(totals, reverse=True)[0:3]))


if __name__ == "__main__":
    main()
