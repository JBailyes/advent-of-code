from aocutils import load_input

import re


def main():

    class Monkey():
        def __init__(self, name:str, job:str) -> None:
            self.name:str = name
            self.number:int = None
            self.m1:str = None
            self.m2:str = None
            self.op:str = None
            if re.match(r'-?\d+', job):
                self.number = int(job)
                self.yell = lambda : self.number
            else:
                m1, op, m2 = job.split()
                self.m1 = m1
                self.m2 = m2
                self.op = op
                self.yell = self._yell_maths


        def _yell_maths(self):
            m1 = monkeys[self.m1]
            m2 = monkeys[self.m2]
            yell_val = None

            if self.op == '+':
                yell_val = m1.yell() + m2.yell()
            elif self.op == '-':
                yell_val = m1.yell() - m2.yell()
            elif self.op == '*':
                yell_val = m1.yell() * m2.yell()
            elif self.op == '/':
                yell_val = m1.yell() / m2.yell()
            
            return int(yell_val)


    monkeys:dict[str, Monkey] = {}

    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    for line in puzzle_input:
        name, job = line.split(': ')
        if name != 'humn':
            monkeys[name] = Monkey(name, job)
    
    root = monkeys['root']
    target_val = monkeys[root.m2].yell()
    print('target:', target_val)

    resolved = False
    resolve_name:str = root.m1
    while not resolved:
        resolve:Monkey = monkeys[resolve_name]
        try:
            known_val = monkeys[resolve.m1].yell()
            if resolve.op == '+':
                target_val -= known_val
            elif resolve.op == '-':
                target_val = known_val - target_val
            elif resolve.op == '*':
                target_val /= known_val
            elif resolve.op == '/':
                target_val = known_val / target_val
            elif resolve.m2 == 'humn':
                print('humn =', target_val)
                exit()
            resolve_name = resolve.m2
        except KeyError:
            known_val = monkeys[resolve.m2].yell()
            if resolve.op == '+':
                target_val -= known_val
            elif resolve.op == '-':
                target_val += known_val
            elif resolve.op == '*':
                target_val /= known_val
            elif resolve.op == '/':
                target_val *= known_val
            if resolve.m1 == 'humn':
                print('humn =', target_val)
                exit()
            resolve_name = resolve.m1
        target_val = int(target_val)

    # Correct answer: 3952673930912


if __name__ == "__main__":
    main()
