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
            my_ticket = [int(n) for n in line.split(',')]
        elif parsing_rules:
            match = re.match(r'^(.*): (.*)$', line)
            name = match.group(1)
            ranges = []
            range_strings = match.group(2).split(' or ')
            for range_string in range_strings:
                ranges.append([int(n) for n in range_string.split('-')])
            rules.append(Rule(name, ranges))

    valid_tickets = []

    positions = len(nearby_tickets[0])

    for nearby_ticket in nearby_tickets:
        ticket_is_valid = True
        for position in range(positions):
            number = nearby_ticket[position]
            valid_for_any_rule = False
            for rule in rules:
                if rule.accepts(number):
                    valid_for_any_rule = True
                    break
            if not valid_for_any_rule:
                ticket_is_valid = False
                break
        if ticket_is_valid:
            valid_tickets.append(nearby_ticket)

    positional_rules = []
    for position in range(positions):
        positional_rules.append(set(rules))

    for nearby_ticket in valid_tickets:
        for position in range(positions):
            number = nearby_ticket[position]
            for rule in rules:
                if not rule.accepts(number):
                    positional_rules[position].discard(rule)

    determined_allocation = {}

    pos_names = []
    for rules in positional_rules:
        pos_names.append(list([rule.name for rule in rules]))

    def remove_rule(name):
        for names in pos_names:
            if len(names) > 1 and name in names:
                names.remove(name)

    while sum([len(names) for names in pos_names]) > positions:
        for names in pos_names:
            if len(names) == 1:
                remove_rule(names[0])
        for position in range(positions):
            names = pos_names[position]
            print('position {} rules: {}'.format(position, names))
        print()

    answer = 1
    for position, names in enumerate(pos_names):
        if names[0].startswith('departure '):
            answer *= my_ticket[position]

    print('answer:', answer)


if __name__ == "__main__":
    main()
