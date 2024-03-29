import os


def load_input(file_name, input_name='input') -> list[str]:
    day = os.path.basename(file_name).split('-')[0]
    challenge_input = os.path.dirname(file_name) + f'/{day}-{input_name}.txt'

    lines = []
    with open(challenge_input, 'r') as infile:
        for line in infile:
            lines.append(line.strip('\n'))

    return lines
