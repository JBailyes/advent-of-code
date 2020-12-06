import argparse
import re
import string
from datetime import datetime
import operator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('scores')
    parser.add_argument('attempts')
    args = parser.parse_args()

    scoreboard = args.scores
    attempts = int(args.attempts)
    print(scoreboard)

    class Elf:
        def __init__(self, initialRecipeIndex):
            self.recipeIndex = initialRecipeIndex
            self.recipe = int(scoreboard[self.recipeIndex])

        def getCurrent(self):
            return self.recipe

        def pickNew(self):
            moveAlong = 1 + self.recipe
            newIndex = (moveAlong + self.recipeIndex) % len(scoreboard)
            newRecipe = int(scoreboard[newIndex])
            self.recipeIndex = newIndex
            self.recipe = newRecipe

        def __str__(self):
            return 'Elf: recipe {0} at index {1}'.format(self.recipe, self.recipeIndex)

    elves = [Elf(0), Elf(1)]
    recipesAdded = [scoreboard[0], scoreboard[1]]

    while len(recipesAdded) < attempts + 10:
    # while len(scoreboard) < attempts + 10:
        curr1 = elves[0].getCurrent()
        curr2 = elves[1].getCurrent()
        newRecipe = str(curr1 + curr2)
        scoreboard += newRecipe
        recipesAdded += newRecipe
        # print('adding ' + newRecipe)
        for elf in elves:
            elf.pickNew()

        # elf1 = elves[0]
        # elf2 = elves[1]
        # for i, score in enumerate(scoreboard):
        #     if elf1.recipeIndex == i:
        #         print('({0})'.format(score), end='')
        #     elif elf2.recipeIndex == i:
        #         print('[{0}]'.format(score), end='')
        #     else:
        #         print(' {0} '.format(score), end='')
        # print()

    print()
    # print('Next 10: ' + scoreboard[attempts:attempts + 10])
    print('Next 10: {0}'.format(''.join(recipesAdded[attempts:attempts + 10])))

    print()
    print('Finish')


if __name__ == "__main__":
    main()
