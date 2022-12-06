from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = ['mjqjpqmgbljsphdztnvjfqwrcgsmlb']

    def is_start_of_packet(text):
        return len(set(text)) == len(text)

    line = puzzle_input[0]
    for i in range(0, len(line) - 13):
        if is_start_of_packet(line[i:i+14]):
            print(i + 14)
            return

    # Correct answer: 2625


if __name__ == "__main__":
    main()
