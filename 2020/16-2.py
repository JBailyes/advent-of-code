import argparse
import os
import re

from aocutils import load_input


class Rule:
    def __init__(self, name, ranges):
        self.name = name
        self.ranges = ranges

    def accepts(self, number):
        for range in self.ranges:
            if range[0] <= number <= range[1]:
                return True
        return False


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    parsing_rules = True
    parsing_mine = False
    parsing_nearby = False

    rules = []
    nearby_tickets = []

    for line in puzzle_input:
        if line == 'your ticket:':
            parsing_mine = True
            continue
        elif line == 'nearby tickets:':
            parsing_nearby = True
            continue
        elif line == '':
            parsing_rules = False
            parsing_mine = False
            parsing_nearby = False
            continue

        if parsing_nearby:
            nearby_tickets.append([int(n) for n in line.split(',')])
        elif parsing_mine:
            pass
        elif parsing_rules:
            match = re.match(r'^(.*): (.*)$', line)
            name = match.group(1)
            ranges = []
            range_strings = match.group(2).split(' or ')
            for range_string in range_strings:
                ranges.append([int(n) for n in range_string.split('-')])
            rules.append(Rule(name, ranges))

    valid_tickets = []

    for nearby_ticket in nearby_tickets:
        for number in nearby_ticket:
            valid_for_any = False
            for rule in rules:
                if rule.accepts(number):
                    valid_for_any = True
                    break
            if valid_for_any:
                valid_tickets.append(nearby_ticket)

    

    print('error rate:', error_rate)


if __name__ == "__main__":
    main()
