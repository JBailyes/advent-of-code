from aocutils import load_input

import re


class Cup:
    def __init__(self, label):
        self.label = label
        self.prev = None
        self.next = None

    def append(self, other):
        other.prev = self
        other.next = self.next
        self.next.prev = other
        self.next = other
        return other

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.prev = None
        self.next = None
        return self

    def prev_label(self) -> int:
        if self.prev is not None:
            return self.prev.label
        return None
    
    def next_label(self) -> int:
        if self.next is not None:
            return self.next.label
        return None

    def __repr__(self):
        return '{}<{}>{}'.format(self.prev_label(), self.label, self.next_label())


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    cups: dict[int, Cup] = {}

    labels = [int(n) for n in puzzle_input[0]]

    MAX_LABEL = 1_000_000
    labels += list(range(len(labels) + 1, MAX_LABEL + 1))

    for label in labels:
        cup = Cup(label)
        cups[label] = cup
    for pos, label in enumerate(labels):
        cups[label].next = cups[labels[(pos + 1) % len(labels)]]
        cups[label].prev = cups[labels[pos - 1]]

    current_cup = cups[labels[0]]

    for move in range(10_000_000):
        removed = [
            current_cup.next.remove(),
            current_cup.next.remove(),
            current_cup.next.remove()]
        removed_labels = [cup.label for cup in removed]

        destination_label = current_cup.label - 1
        while destination_label in removed_labels or destination_label == 0:
            if destination_label == 0:
                destination_label = MAX_LABEL
            else:
                destination_label -= 1

        dest_cup = cups[destination_label]

        dest_cup.append(removed[0]).append(removed[1]).append(removed[2])
        current_cup = current_cup.next

    cup1 = cups[1]
    first_clockwise = cup1.next
    second_clockwise = cup1.next.next
    print('1st and 2nd clockwise:', first_clockwise, second_clockwise)
    print('Multiplied:', first_clockwise.label * second_clockwise.label)


if __name__ == "__main__":
    main()
