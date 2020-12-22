from aocutils import load_input

import re


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    puzzle_input.append('')

    player_decks: list[list[int]] = []
    all_input = '\n'.join(puzzle_input)
    for player_deck_match in re.finditer(r'Player (\d+):\n([\d\n]*[^\n])\n', all_input):
        deck = [int(card) for card in player_deck_match.group(2).split('\n')]
        player_decks.append(deck)

    NOBODY = -1
    PLAYER_1 = 0
    PLAYER_2 = 1

    def play(p1_deck, p2_deck) -> int:

        previous_rounds = []
        number_of_cards = len(p1_deck) + len(p2_deck)

        winner = NOBODY
        while winner == NOBODY:
            this_round = [p1_deck.copy(), p2_deck.copy()]

            if this_round in previous_rounds:
                return PLAYER_1

            previous_rounds.append(this_round)

            p1_card = p1_deck.pop(0)
            p2_card = p2_deck.pop(0)

            if len(p1_deck) >= p1_card and len(p2_deck) >= p2_card:
                round_winner = play(p1_deck[:p1_card], p2_deck[:p2_card])
            else:
                if p1_card > p2_card:
                    round_winner = PLAYER_1
                else:
                    round_winner = PLAYER_2

            if round_winner == PLAYER_1:
                p1_deck += [p1_card, p2_card]
                if len(p1_deck) == number_of_cards:
                    winner = PLAYER_1
            else:
                p2_deck += [p2_card, p1_card]
                if len(p2_deck) == number_of_cards:
                    winner = PLAYER_2

        return winner

    overall_winner = play(player_decks[PLAYER_1], player_decks[PLAYER_2])
    winning_deck = player_decks[overall_winner]

    score = sum([card * pos for card, pos in zip(winning_deck, range(len(winning_deck), 0, -1))])
    print(score)


if __name__ == "__main__":
    main()
