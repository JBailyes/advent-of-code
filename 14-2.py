import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore,  Back,  Style
from typing import List
from os.path import basename
import math

from computer import Computer


class ChemicalSpec:
    def __init__(self, num, name):
        self.num: int = num
        self.name: str = name

    @staticmethod
    def from_str(definition: str):
        (num_str, name) = definition.strip().split(' ')
        return ChemicalSpec(int(num_str), name)

    def __str__(self):
        return '{0} {1}'.format(self.num, self.name)

    def __repr__(self):
        return str(self)


class Reaction:
    def __init__(self, ingredients: List[ChemicalSpec], result: ChemicalSpec):
        self.ingredients = ingredients
        self.result: ChemicalSpec = result

    @staticmethod
    def from_str(definition: str):
        (ingredients, result) = definition.split(' => ')

        ingredient_list = []
        for ingredient in ingredients.split(', '):
            ingredient_list.append(ChemicalSpec.from_str(ingredient))

        return Reaction(ingredient_list, ChemicalSpec.from_str(result))

    def name(self) -> str:
        return self.result.name

    def __str__(self):
        return '{0} => {1}'.format(self.ingredients, self.result)

    def __repr__(self):
        return str(self)


class Nanofactory:
    def __init__(self, reaction_definitions: List[Reaction]):
        self.reaction_defs = {}
        self.chemical_store = {'ORE': 0}
        self.order_total = {'ORE': 0}
        for reaction in reaction_definitions:
            self.reaction_defs[reaction.name()] = reaction
            self.chemical_store[reaction.name()] = 0
            self.order_total[reaction.name()] = 0

    def consume(self, order_size: int, name: str):
        # print('consuming {0} {1}'.format(order_size, name))

        stock = self.chemical_store[name]
        if order_size <= stock:
            self.chemical_store[name] -= order_size
            return
        extra_needed = order_size - stock
        self.chemical_store[name] = 0

        if name == 'ORE':
            self.order_total[name] += extra_needed
            return

        reaction = self.reaction_defs[name]
        reaction_yield = reaction.result.num
        reactions_needed = 1
        if reaction_yield < extra_needed:
            reactions_needed = int(extra_needed / reaction_yield)
            if extra_needed % reaction_yield != 0:
                reactions_needed += 1

        # print('   {0} {1} reactions needed'.format(reactions_needed, name))
        for chem_spec in reaction.ingredients:
            self.consume(chem_spec.num * reactions_needed, chem_spec.name)
        self.chemical_store[name] += reactions_needed * reaction_yield - extra_needed


reactions = {}
multiples = {}


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    # inputFile = basename(__file__)[:2] + '-example-1.txt'
    # inputFile = basename(__file__)[:2] + '-example-2.txt'
    # inputFile = basename(__file__)[:2] + '-example-3.txt'
    # inputFile = basename(__file__)[:2] + '-example-4.txt'
    # inputFile = basename(__file__)[:2] + '-example-5.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    for line in lines:
        reaction = Reaction.from_str(line)
        print('loaded:', reaction)
        reactions[reaction.result.name] = reaction

    factory = Nanofactory(list(reactions.values()))

    print('')
    fuel_count = -1
    while factory.order_total['ORE'] < 1000000000000:
        fuel_count += 1
        if fuel_count % 1000 == 0:
            print('made {0} fuel from {1} ore'.format(
                fuel_count, format(factory.order_total['ORE'], ',d')))
        factory.consume(1, 'FUEL')
    print('')
    print('made {0} fuel from {1} ore'.format(fuel_count, factory.order_total['ORE']))


if __name__ == "__main__":
    main()
