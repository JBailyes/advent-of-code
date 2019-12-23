from os.path import basename
from typing import List

import colorama
import re

from computer import Computer


class Stack:
    def __init__(self, num_cards: int, watch_pos: int):
        self.num_cards = num_cards
        self.pos_pointer: int = watch_pos

    def undo_deal_new_stack(self):
        self.pos_pointer = (self.num_cards - 1) - self.pos_pointer

    def undo_cut_cards(self, n: int):
        self.pos_pointer = (self.pos_pointer + n) % self.num_cards

    def undo_deal_with_increment(self, n: int):
        # (a * n) % num_cards == pos_pointer
        # Only one value could have resulted in the current position pointer
        loop_count = 0
        pre_deal_pos = self.pos_pointer / n
        while not pre_deal_pos.is_integer():
            loop_count += 1
            pre_deal_pos = (loop_count * self.num_cards + self.pos_pointer) / n
        self.pos_pointer = int(pre_deal_pos)

    def undo(self, technique: str):
        if technique == 'deal into new stack':
            self.undo_deal_new_stack()
        elif technique.startswith('cut '):
            self.undo_cut_cards(int(technique.split(' ')[-1]))
        elif technique.startswith('deal with increment '):
            self.undo_deal_with_increment(int(technique.split(' ')[-1]))


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    # lines = [
        # 'deal with increment 7',
        # 'deal into new stack',
        # 'deal into new stack'

        # 'cut 6',
        # 'deal with increment 7',
        # 'deal into new stack'

        # 'deal with increment 7',
        # 'deal with increment 9',
        # 'cut -2'

        # 'deal into new stack',
        # 'cut -2',
        # 'deal with increment 7',
        # 'cut 8',
        # 'cut -4',
        # 'deal with increment 7',
        # 'cut 3',
        # 'deal with increment 9',
        # 'deal with increment 3',
        # 'cut -1'
    # ]

    lines.reverse()

    # stack_size = 10
    # for pos in range(0, stack_size):
    #     stack = Stack(stack_size, pos)
    #     for technique in lines:
    #         stack.undo(technique)
    #     print(stack.pos_pointer, end=' ')
    # print('')

    stack_size = 119_315_717_514_047
    stack = Stack(stack_size, 2020)
    for i in range(0, 101741582076661):
        if i % 1000 == 0:
            print('loop', i)
        for technique in lines:
            stack.undo(technique)
    print(stack.pos_pointer)
    # repeats = 0
    # loop_count = 0
    # while repeats == 0:
    #     for technique in lines:
    #         stack.undo(technique)
    #     loop_count += 1
    #     if loop_count % 100 == 0:
    #         print('loop', loop_count)
    #     value = stack.pos_pointer
    #     if value == first:
    #         repeats = 1
    #         print(value, 'at', loop_count)




if __name__ == "__main__":
    main()
