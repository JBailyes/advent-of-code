import os


def load_input(file_name, input_name=None) -> list[str]:
    day = os.path.basename(file_name).split('-')[0]
    if input_name is None:
        input_name = 'input'
    challenge_input = '{}-{}.txt'.format(day, input_name)

    lines = []
    with open(challenge_input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    return lines
