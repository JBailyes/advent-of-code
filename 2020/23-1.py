from aocutils import load_input


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
    for label in labels:
        cup = Cup(label)
        cups[label] = cup
    for pos, label in enumerate(labels):
        cups[label].next = cups[labels[(pos + 1) % len(labels)]]
        cups[label].prev = cups[labels[pos - 1]]

    current_cup = cups[labels[0]]

    for move in range(100):
        removed = [
            current_cup.next.remove(),
            current_cup.next.remove(),
            current_cup.next.remove()]
        removed_labels = set([cup.label for cup in removed])

        labels_in_circle = sorted(list(set(labels) - removed_labels))
        destination_label = labels_in_circle[labels_in_circle.index(current_cup.label) - 1]
        dest_cup = cups[destination_label]

        dest_cup.append(removed[0]).append(removed[1]).append(removed[2])
        current_cup = current_cup.next

    end_state = ''
    cup = cups[1]
    for i in range(len(cups) - 1):
        cup = cup.next
        end_state += str(cup.label)
    print('End state:', end_state)


if __name__ == "__main__":
    main()
