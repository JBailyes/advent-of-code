import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore,  Back,  Style
from os.path import basename
import math


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())
    data = lines[0]

    # data = "123456789012"

    width = 25
    height = 6
    layer_size = width * height

    layer_count = int(len(data) / layer_size)
    print(layer_count, "layers")

    layers = list()

    for i in range(0, layer_count):
        layer_data = ''
        for y in range(0, height):
            for x in range(0, width):
                digit = data[i * layer_size + y * width + x]
                layer_data += digit
        layers.append(layer_data)

    image = []
    for i in range(0, layer_size):
        image.append('0')

    layers.reverse()
    for layer in layers:
        for y in range(0, height):
            for x in range(0, width):
                pixel_index = y * width + x
                pixel_value = layer[pixel_index]
                if pixel_value in ['0', '1']:
                    image[pixel_index] = pixel_value

    for y in range(0, height):
        for x in range(0, width):
            pixel_index = y * width + x
            pixel_value = image[pixel_index]
            if pixel_value == '0':
                pixel_value = ' '
            print(pixel_value, end='')
        print('')


if __name__ == "__main__":
    main()
