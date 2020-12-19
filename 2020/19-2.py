from aocutils import load_input

import re


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')
    # puzzle_input = load_input(__file__, 'example2')

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
                if '|' in rule_regex:
                    rule = '(' + rule_regex + ')'
                else:
                    rule = rule_regex
                updated_rule = re.sub(r'\b{}\b'.format(rule_number), rule, updated_rule)
            if not re.search(r'\d', updated_rule):
                rules[unresolved_rule_number] = updated_rule.replace(' ', '')

        for rule_number in rules.keys():
            unresolved_rules.pop(rule_number, None)
        print(unresolved_rules)

    rules[8] = '(' + rules[8] + ')+'
    rules[0] = r'({})({})+({})+'.format(rules[42], rules[42], rules[31])

    print('Rules:')
    for number, rule in sorted(rules.items()):
        print(number, ':', rule)

    def rule0(text):
        # Use named groups because the inserted rules will be full of groups too
        even_42_31 = r'(?P<r42>{})(?P<middle>.+)(?P<r31>{})'.format(rules[42], rules[31])

        # Must have at least one top-level match of this pattern for rule 0 to be valid
        rule0_match = re.fullmatch(even_42_31, text)
        if rule0_match:
            # This inner rule could potentially only match rule 42
            return rule0_inner(rule0_match.group('middle'))
        return False

    def rule0_inner(text):
        # Use named groups because the inserted rules will be full of groups too
        even_42_31 = r'(?P<r42>{})(?P<middle>.+)(?P<r31>{})'.format(rules[42], rules[31])

        rule0_match = re.fullmatch(even_42_31, text)
        if rule0_match:
            return rule0_inner(rule0_match.group('middle'))
        if re.fullmatch(r'({})+'.format(rules[42]), text):
            return True
        return False

    matches = 0
    for message in messages:
        if rule0(message):
            matches += 1

    print('matches:', matches)


if __name__ == "__main__":
    main()
