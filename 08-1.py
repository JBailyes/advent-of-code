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

    layers = []
    fewest_zeros = layer_size
    fewest_zeros_layer = ''

    for i in range(0, layer_count):
        print("Layer", i)
        layer_data = ''
        for y in range(0, height):
            for x in range(0, width):
                digit = data[i * layer_size + y * width + x]
                layer_data += digit
        layers.append(layer_data)
        zero_count = layer_data.count('0')
        if zero_count < fewest_zeros:
            fewest_zeros = zero_count
            fewest_zeros_layer = layer_data

    ones_count = fewest_zeros_layer.count('1')
    twos_count = fewest_zeros_layer.count('2')

    print(ones_count * twos_count)

if __name__ == "__main__":
    main()
