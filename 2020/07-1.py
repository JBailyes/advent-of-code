import argparse
import re


class Rule:
    def __init__(self, number, bag):
        self.number = number
        self.bag = bag

    def __repr__(self):
        return '{} {}'.format(self.number, self.bag)


class Bag:
    def __init__(self, colour, rules=None):
        self.colour = colour
        if not rules:
            self.rules = []
        else:
            self.rules = rules
        self.contained_by = []

    def __repr__(self):
        return '{} {}'.format(self.colour, self.rules)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    shiny_gold = 'shiny gold'
    shiny_gold_holders = set()
    bags = {}

    def get_bag(colour):
        if colour not in bags:
            bags[colour] = Bag(colour)
        return bags[colour]

    for rule in lines:
        match = re.match(r'([\w ]+) bags contain (.*)$', rule)
        bag_colour = match.group(1)
        contents = match.group(2)
        container_bag = get_bag(bag_colour)
        if contents != 'no other bags.':
            for contained in contents.split(','):
                contained_match = re.match(r'\s*(\d+) ([\w ]+) bags?', contained)
                contained_number = int(contained_match.group(1))
                contained_colour = contained_match.group(2)
                contained_bag = get_bag(contained_colour)
                contained_bag.contained_by.append(container_bag)
                container_bag.rules.append(Rule(contained_number, contained_colour))

    print(bags.keys())

    def follow_the_gold(bag):
        for container in bag.contained_by:
            shiny_gold_holders.add(container)
            follow_the_gold(container)

    follow_the_gold(bags[shiny_gold])

    # 274 is the right answer for my input
    print(len(shiny_gold_holders))


if __name__ == "__main__":
    main()
