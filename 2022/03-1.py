import string

from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    string.ascii_letters
    sum = 0

    for line in puzzle_input:
        half = int(len(line)/2)
        sack_1 = set(line[0:half])
        sack_2 = set(line[half:])

        common = sack_1 & sack_2
        for item_type in common:
            sum += string.ascii_letters.find(item_type) + 1

    print(sum)
    
    # Correct answer: 8401


if __name__ == "__main__":
    main()
