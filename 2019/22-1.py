from os.path import basename
from typing import List

import colorama
import re

from computer import Computer


class Stack:
    def __init__(self, num_cards: int):
        self.num_cards = num_cards
        self.cards: List[int] = list(range(0, num_cards))

    def deal_into_new_stack(self):
        self.cards.reverse()
        return self

    def cut_cards(self, n: int):
        new_stack = self.cards[n:] + self.cards[:n]
        self.cards = new_stack
        return self

    def deal_with_increment(self, n: int):
        new_stack = self.cards.copy()
        for pos, card in enumerate(self.cards):
            new_pos = (pos * n) % self.num_cards
            new_stack[new_pos] = card
        self.cards = new_stack
        return self

    def perform(self, technique: str):
        if technique == 'deal into new stack':
            self.deal_into_new_stack()
        elif technique.startswith('cut '):
            self.cut_cards(int(technique.split(' ')[-1]))
        elif technique.startswith('deal with increment '):
            self.deal_with_increment(int(technique.split(' ')[-1]))
        return self


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    # stack = Stack(10)
    # lines = [
    #     # 'deal with increment 7',
    #     # 'deal into new stack',
    #     # 'deal into new stack'
    #
    #     # 'cut 6',
    #     # 'deal with increment 7',
    #     # 'deal into new stack'
    #
    #     'deal into new stack',
    #     'cut -2',
    #     'deal with increment 7',
    #     'cut 8',
    #     'cut -4',
    #     'deal with increment 7',
    #     'cut 3',
    #     'deal with increment 9',
    #     'deal with increment 3',
    #     'cut -1'
    # ]

    stack = Stack(10_007)

    for technique in lines:
        stack.perform(technique)

    for pos, card in enumerate(stack.cards):
        if card == 2019:
            print(pos)

    # 8440 is too high


if __name__ == "__main__":
    main()
