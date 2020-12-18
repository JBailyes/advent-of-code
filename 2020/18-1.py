import argparse
import os
import re

from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    def evaluate(expression) -> int:
        if '(' not in expression:
            return evaluate_operation(expression)
        match = re.search(r'\(([^()]+)\)', expression)
        number = evaluate_operation(match.group(1))
        return evaluate(expression[0:match.start()] + str(number) + expression[match.end():])

    def evaluate_operation(expression) -> int:
        if re.match(r'^\d+$', expression):
            return int(expression)
        match = re.match(r'(.*) ([+*]) (\d+)', expression)
        l_num = evaluate_operation(match.group(1))
        operator = match.group(2)
        r_num = int(match.group(3))
        if operator == '+':
            return l_num + r_num
        elif operator == '*':
            return l_num * r_num

    print(evaluate_operation('1 + 2 * 3 + 4 * 5 + 6'))
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
