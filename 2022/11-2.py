from aocutils import load_input


def main():

    monkeys:dict = {}

    class Monkey():
        def __init__(self, items:list[int],
                            op_type:str,
                            op_val:str,
                            divisor:int,
                            true_m:int,
                            false_m:int) -> None:
            self.items = items
            self.op_type = op_type
            self.op_val = op_val
            self.divisor = divisor
            self.true_monkey = true_m
            self.false_monkey = false_m
            self.inspections:int = 0
        
        def take_turn(self):
            while len(self.items):
                self.inspect_item(self.items.pop(0))

        def inspect_item(self, worry:int):
            self.inspections += 1
            operand:int = 0
            if self.op_val == 'old':
                operand = worry
            else:
                operand = int(self.op_val)
            if self.op_type == '*':
                worry *= operand
            elif self.op_type == '+':
                worry += operand
            
            worry %= worry_check

            if worry % self.divisor == 0:
                target = monkeys[self.true_monkey]
            else:
                target = monkeys[self.false_monkey]
            target.items.append(worry)


    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    for line_num in range(0, len(puzzle_input) + 1, 7):
        for line in puzzle_input[line_num:line_num+7]:
            if line.startswith('Monkey'):
                monkey_num = int(line.split(' ')[1].split(':')[0])
                print('monkey', monkey_num)
            elif 'Starting items:' in line:
                items = [int(i) for i in line.split(': ')[1].split(', ')]
                print('items', items)
            elif 'Operation:' in line:
                op, val = line.split('= old ')[1].split(' ')
                print('op', op, val)
            elif 'Test: divisible' in line:
                divisor = int(line.split(' ')[-1])
                print('div by', divisor)
            elif 'If true' in line:
                true_target = int(line.split(' ')[-1])
                print('if true monkey', true_target)
            elif 'If false' in line:
                false_target = int(line.split(' ')[-1])
                print('if false monkey', false_target)
        monkey = Monkey(items, op, val, divisor, true_target, false_target)
        monkeys[monkey_num] = monkey
    
    worry_check = 1
    for monkey in monkeys.values():
        worry_check *= monkey.divisor

    print()
    print()
    rounds = 10_000
    for round in range(rounds):
        # print('round ', round)
        if round % 100 == 0:
            print('round', round)
        for monkey_num in sorted(monkeys):
            monkeys[monkey_num].take_turn()

    
    inspection_counts:list[int] = []
    for monkey_num in sorted(monkeys):
        inspection_counts.append(monkeys[monkey_num].inspections)
        print(f'monkey {monkey_num} did {monkeys[monkey_num].inspections} inspections')

    inspection_counts.sort()
    business = inspection_counts[-2] * inspection_counts[-1]
    print('business', business)

    # Correct answer: 32059801242


if __name__ == "__main__":
    main()
