from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    def defeats(one, other):
        if (one in 'AX'):
            return other in 'CZ'
        if (one in 'CZ'):
            return other in 'BY'
        if (one in 'BY'):
            return other in 'AX'
        return False

    score = 0

    for line in puzzle_input:
        opponent, me = line.split()

        draw = line in ['A X', 'B Y', 'C Z']
        win = defeats(me, opponent)
        lose = defeats(opponent, me)

        round_score = { 'X': 1, 'Y': 2, 'Z': 3}[me]
        if draw:
            round_score += 3
        elif win:
            round_score += 6
        score += round_score

    print(score)
    
    # Correct answer: 12679


if __name__ == "__main__":
    main()
