from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    totals = []

    current_total = 0
    for line in puzzle_input:
        if line == '':
            totals.append(current_total)
            current_total = 0
        else:
            current_total += int(line)  # Bug that didn't happen to affect my input: the last line inthe file won't get added to the total
    
    # Correct answer: 69289
    print(max(totals))


if __name__ == "__main__":
    main()
