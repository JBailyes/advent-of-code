from aocutils import load_input
import re

def main():
    puzzle_input_moves = load_input(__file__)
    puzzle_input_start = load_input(__file__, 'start')
    # puzzle_input_start = load_input(__file__, 'example-start')
    # puzzle_input_moves = load_input(__file__, 'example')

    stack_positions = list(range(1,36,4))
    # stack_positions = list(range(1,10,4))
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

        mini_stack = []
        for _ in range(0, num_to_move):
            mini_stack.append(stacks[from_stack].pop())
        mini_stack.reverse()
        stacks[to_stack] += mini_stack

    for stack in stacks:
        if stack:
            print(stack[-1], end='')
        else:
            print(' ', end='')
    print()

    # Correct answer: LCTQFBVZV


if __name__ == "__main__":
    main()
