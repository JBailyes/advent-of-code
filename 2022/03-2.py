import string

from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    string.ascii_letters
    sum = 0

    line_num = 0
    while line_num < len(puzzle_input):
        rucksacks = puzzle_input[line_num:line_num+3]
        sack_1 = set(rucksacks[0])
        sack_2 = set(rucksacks[1])
        sack_3 = set(rucksacks[2])

        common_type = list(sack_1 & sack_2 & sack_3)[0]
        sum += string.ascii_letters.find(common_type) + 1
        line_num += 3

    print(sum)
    
    # Correct answer: 2641


if __name__ == "__main__":
    main()
