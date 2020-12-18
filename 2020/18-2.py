import argparse
import os
import re

from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    def evaluate(expression) -> int:
        if '(' not in expression:
            return evaluate_operations(expression)
        match = re.search(r'\(([^()]+)\)', expression)
        number = evaluate_operations(match.group(1))
        return int(evaluate(expression[0:match.start()] + str(number) + expression[match.end():]))

    def evaluate_operations(expression) -> int:
        additions_done = evaluate_additions(expression)
        return int(evaluate_multiplications(additions_done))

    def evaluate_additions(expression) -> str:
        match = re.search(r'(\d+) \+ (\d+)', expression)
        evaluated = expression
        if match:
            number = int(match.group(1)) + int(match.group(2))
            evaluated = evaluate_additions(expression[0:match.start()] + str(number) + expression[match.end():])
        return evaluated

    def evaluate_multiplications(expression) -> str:
        match = re.search(r'(\d+) \* (\d+)', expression)
        evaluated = expression
        if match:
            number = int(match.group(1)) * int(match.group(2))
            evaluated = evaluate_multiplications(expression[0:match.start()] + str(number) + expression[match.end():])
        return evaluated

    print(evaluate('1 + 2 * 3 + 4 * 5 + 6'))
    print(evaluate('1 + (2 * 3) + (4 * (5 + 6))'))
    print(evaluate('2 * 3 + (4 * 5)'))
    print(evaluate('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
    print(evaluate('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
    print(evaluate('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))

    sum = 0
    for expression in puzzle_input:
        sum += evaluate(expression)
    print('Homework sum:', sum)


if __name__ == "__main__":
    main()
