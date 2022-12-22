from aocutils import load_input

import re


def main():

    class Monkey():
        def __init__(self, name:str, job:str) -> None:
            self.name:str = name
            self.number:int = None
            self.m1 = None
            self.m2 = None
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
            
            if self.name == 'root' and yell_val is not None:
                print('root:', yell_val)
                exit()
            else:
                return yell_val


    monkeys:dict[str, Monkey] = {}

    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    for line in puzzle_input:
        name, job = line.split(': ')
        monkeys[name] = Monkey(name, job)
    
    root = monkeys['root']
    root.yell()

    # Correct answer: 54703080378102


if __name__ == "__main__":
    main()
