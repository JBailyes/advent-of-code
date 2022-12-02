from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    # Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock
    # A for Rock, B for Paper, and C for Scissors

    def defeat(item):
        if item == 'A':
            return 'B'
        if item == 'C':
            return 'A'
        if item == 'B':
            return 'C'

    def lose(item):
        if item == 'A':
            return 'C'
        if item == 'C':
            return 'B'
        if item == 'B':
            return 'A'

    score = 0

    for line in puzzle_input:
        opponent, outcome = line.split()

        # X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win

        if outcome == 'Y':
            mine = opponent
            score += 3
        elif outcome == 'Z':
            mine = defeat(opponent)
            score += 6
        else:
            mine = lose(opponent)

        score += { 'A': 1, 'B': 2, 'C': 3}[mine]

    print(score)
    
    # Correct answer: 14470


if __name__ == "__main__":
    main()
