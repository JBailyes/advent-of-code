import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore, Back, Style
from os.path import basename
import math


def meets_criteria(password):
    # print(password)
    runs = set()
    current_run = password[0]
    for digit in password[1:]:
        if digit < current_run[-1]:
            return False
        if digit == current_run[-1]:
            current_run += digit
        else:
            runs.add(len(current_run))
            # print('  ' + current_run)
            current_run = digit
    runs.add(len(current_run))
    # print('  ' + current_run)

    return 2 in runs


def main():
    colorama.init()

    print(meets_criteria('122345'))
    print(meets_criteria('111111'))
    print(meets_criteria('223450'))
    print(meets_criteria('123789'))
    print(meets_criteria('123444'))
    print(meets_criteria('122255'))

    matches = 0
    for number in range(367479, 893699):
        if meets_criteria(str(number)):
            matches += 1
    print(matches)

    # 149 - wrong
    # 214 - wrong
    # 305 - correct


if __name__ == "__main__":
    main()
