from aocutils import load_input
import re

def main():
    puzzle_input_moves = load_input(__file__)
    puzzle_input_start = load_input(__file__, 'start')
    # puzzle_input_start = load_input(__file__, 'example-start')
    # puzzle_input_moves = load_input(__file__, 'example')

    stack_positions = [list(range(1,36,4))]
    load_stacks = [[], [], [], [], [], [], [], [], []]
    stacks = []

    for line in puzzle_input_start:
        for stack,stack_pos in enumerate(stack_positions):
            crate = line[stack_pos]
            if crate != ' ':
                load_stacks[stack].append(crate)
    
    for stack_num in range(0, len(load_stacks)):
        stacks.append(list(reversed(load_stacks[stack_num])))

    print(stacks)

    for line in puzzle_input_moves:
        match = re.match(r'move (\d+) from (\d+) to (\d+)', line)
        if not match:
            continue

        num_to_move = int(match.group(1))
        from_stack = int(match.group(2)) - 1
        to_stack = int(match.group(3)) - 1

        for _ in range(0, num_to_move):
            crate = stacks[from_stack].pop()
            stacks[to_stack].append(crate)

    for stack in stacks:
        print(stack[-1], end='')
    print()

    # Correct answer: VJSFHWGFT


if __name__ == "__main__":
    main()
