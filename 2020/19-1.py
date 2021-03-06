from aocutils import load_input

import re


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    unresolved_rules = {}
    rules = {}
    messages = []
    for line in puzzle_input:
        match = re.match(r'^(\d+): (.*)', line)
        if match:
            rule_number = int(match.group(1))
            rule_text = match.group(2)
            if '"' in rule_text:
                rules[rule_number] = rule_text[1]
            else:
                unresolved_rules[rule_number] = rule_text
        elif line == '':
            pass
        else:
            messages.append(line)

    while len(unresolved_rules) > 0:
        for unresolved_rule_number, unresolved_rule in unresolved_rules.items():
            updated_rule = unresolved_rule
            for rule_number, rule_regex in rules.items():
                if len(rule_regex) == 1:
                    rule = rule_regex
                else:
                    rule = '({})'.format(rule_regex)
                updated_rule = re.sub(r'\b{}\b'.format(rule_number), rule, updated_rule)
            if not re.search(r'\d', updated_rule):
                rules[unresolved_rule_number] = updated_rule.replace(' ', '')

        for rule_number in rules.keys():
            unresolved_rules.pop(rule_number, None)
        print(unresolved_rules)

    print('Rules:')
    for number, rule in sorted(rules.items()):
        print(number, ':', rule)

    matches = 0
    for message in messages:
        if re.fullmatch(rules[0], message):
            matches += 1
    print('matches:', matches)


if __name__ == "__main__":
    main()
