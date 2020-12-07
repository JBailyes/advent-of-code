import argparse
import re


class Rule:
    def __init__(self, number, bag):
        self.number = number
        self.bag = bag

    def __repr__(self):
        return '{} {}'.format(self.number, self.bag)


class Bag:
    def __init__(self, colour):
        self.colour = colour
        self.rules = []
        self.inner_bag_count = -1

    def count_bags(self):
        if self.inner_bag_count != -1:
            return self.inner_bag_count

        self.inner_bag_count = 0
        for rule in self.rules:
            self.inner_bag_count += rule.number + rule.bag.count_bags() * rule.number
        return self.inner_bag_count

    def __repr__(self):
        return '{} {} {}'.format(self.colour, self.rules, self.inner_bag_count)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    shiny_gold = 'shiny gold'
    bags = {}

    def get_bag(colour):
        if colour not in bags:
            bags[colour] = Bag(colour)
        return bags[colour]

    for rule in lines:
        match = re.match(r'([\w ]+) bags contain (.*)$', rule)
        bag_colour = match.group(1)
        contents = match.group(2)
        outer_bag = get_bag(bag_colour)
        if contents == 'no other bags.':
            outer_bag.inner_bag_count = 0
        else:
            for inner in contents.split(','):
                inner_match = re.match(r'\s*(\d+) ([\w ]+) bags?', inner)
                inner_number = int(inner_match.group(1))
                inner_colour = inner_match.group(2)
                inner_bag = get_bag(inner_colour)
                outer_bag.rules.append(Rule(inner_number, inner_bag))

    print(bags.keys())

    # 158730 bags!
    print(get_bag(shiny_gold).count_bags())


if __name__ == "__main__":
    main()
