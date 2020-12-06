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
    consecutives = False
    last_digit = password[0]
    for digit in password[1:]:
        if digit < last_digit:
            return False
        consecutives |= digit == last_digit
        last_digit = digit
    return consecutives


def main():
    colorama.init()

    print(meets_criteria('122345'))
    print(meets_criteria('111111'))
    print(meets_criteria('223450'))
    print(meets_criteria('123789'))

    matches = 0;
    for number in range(367479, 893699):
        if meets_criteria(str(number)):
            matches += 1
    print(matches)

    # 495 - correct


if __name__ == "__main__":
    main()
