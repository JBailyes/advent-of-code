from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    count = 0

    for line in puzzle_input:
        elf_1, elf_2 = line.split(',')
        elf_1_start, elf_1_end = [int(s) for s in elf_1.split('-')]
        elf_2_start, elf_2_end = [int(s) for s in elf_2.split('-')]
        elf_1_assigned = set(range(elf_1_start, elf_1_end + 1))
        elf_2_assigned = set(range(elf_2_start, elf_2_end + 1))

        overlap = elf_1_assigned & elf_2_assigned
        if overlap == elf_1_assigned or overlap == elf_2_assigned:
            count += 1

    print(count)
    
    # Correct answer: 511


if __name__ == "__main__":
    main()
