import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    passports = []

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())
    if lines[-1] != '':
        lines.append('')

    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

    valid = []

    passport = {}
    for line in lines:
        if line == '':
            if len(set(passport.keys()) & required_fields) == len(required_fields):
                valid.append(passport)
            passport = {}
        else:
            for field in line.split(' '):
                field_name, field_value = field.split(':', maxsplit=1)
                passport[field_name] = field_value

    print('Valid passports:', len(valid))


if __name__ == "__main__":
    main()
