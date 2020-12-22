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

    number_of_cards = sum([len(deck) for deck in player_decks])

    while max([len(deck) for deck in player_decks]) != number_of_cards:
        p1 = player_decks[0].pop(0)
        p2 = player_decks[1].pop(0)

        if p1 > p2:
            player_decks[0].append(p1)
            player_decks[0].append(p2)
        elif p2 > p1:
            player_decks[1].append(p2)
            player_decks[1].append(p1)
        else:
            pass  # Rules don't say what happens if the cards are the same

    winning_deck = player_decks[0]
    if len(player_decks[1]) > 0:
        winning_deck = player_decks[1]

    score = sum([card * pos for card, pos in zip(winning_deck, range(number_of_cards, 0, -1))])
    print(score)


if __name__ == "__main__":
    main()
