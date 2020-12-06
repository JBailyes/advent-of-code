import argparse
import re


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

    def is_field_valid(name, value):
        if name == 'byr':
            return re.match(r'\d{4}$', value) and 1920 <= int(value) <= 2002

        elif name == 'iyr':
            return re.match(r'\d{4}$', value) and 2010 <= int(value) <= 2020

        elif name == 'eyr':
            return re.match(r'\d{4}$', value) and 2020 <= int(value) <= 2030

        elif name == 'hgt':
            match = re.match(r'(\d{2,3})(cm|in)$', value)
            if match and match.group(2) == 'cm':
                return 150 <= int(match.group(1)) <= 193
            return match and match.group(2) == 'in' and 59 <= int(match.group(1)) <= 76

        elif name == 'hcl':
            match = re.match(r'#[0-9a-f]{6}$', value)
            return match

        elif name == 'ecl':
            return value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

        elif name == 'pid':
            return re.match(r'\d{9}$', value)

        else:
            return True

    def is_passport_valid(passport):
        if len(set(passport.keys()) & required_fields) != len(required_fields):
            return False
        for name, value in passport.items():
            if not is_field_valid(name, value):
                return False
        return True

    valid = []

    passport = {}
    for line in lines:
        if line == '':
            if is_passport_valid(passport):
                valid.append(passport)
            passport = {}
        else:
            for field in line.split(' '):
                field_name, field_value = field.split(':', maxsplit=1)
                passport[field_name] = field_value

    # 103 is correct for my input
    print('Valid passports:', len(valid))


if __name__ == "__main__":
    main()
