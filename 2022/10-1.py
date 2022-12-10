from aocutils import load_input


def main():


    class CPU():
        def __init__(self) -> None:
            self.x = 1
            self.cycle = 0
            self.op = None
            self.op_end = 0
            self.v = 0

        def start_cycle(self):
            self.cycle += 1

        def end_cycle(self):
            if self.cycle == self.op_end:
                if self.op == 'addx':
                    self.x += self.v
                self.op = None

        def addx(self, v):
            self.op = 'addx'
            self.v = v
            self.op_end = self.cycle + 2

        def noop(self):
            self.op = 'noop'
            self.op_end = self.cycle + 1


    instructions = load_input(__file__)
    # instructions = load_input(__file__, 'example')
    # instructions = load_input(__file__, 'example-2')

    cpu = CPU()
    signal_strengths = []

    for line in instructions:
        # print(line)
        if line.startswith('addx'):
            v = int(line.split(' ')[1])
            cpu.addx(v)
        
        if line.startswith('noop'):
            cpu.noop()
        
        while not cpu.op is None:
            cpu.start_cycle()
            if (cpu.cycle + 20) % 40 == 0:
                signal_strengths.append(cpu.cycle * cpu.x)
            # print(cpu.cycle)
            # print(cpu.x)
            cpu.end_cycle()

    print(cpu.x)

    print(signal_strengths)
    print(sum(signal_strengths))

    # Correct answer: 13180


if __name__ == "__main__":
    main()
