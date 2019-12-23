class NetworkedComputer:
    def __init__(self, programme, inputs, debug=False):
        self._memory = {}
        self._inputs = inputs
        self._outputs = []
        self._instruction_pointer = 0
        self._relative_base = 0
        self._state = 'init'
        self._debug = debug

        for address in range(0, len(programme)):
            self._write(address, programme[address])

    def input(self, value):
        self._inputs.append(value)

    def has_inputs(self):
        return len(self._inputs) > 0

    def read(self):
        if len(self._outputs) > 0:
            return self._outputs.pop(0)
        return None

    def outputs(self):
        return self._outputs.copy()

    def has_output(self):
        return len(self._outputs) > 0

    def state(self):
        return self._state

    def tick(self):
        instruction = '{0:05}'.format(self._read(self._instruction_pointer))
        opcode = int(instruction[-2:])
        param_1_mode = int(instruction[2])
        param_2_mode = int(instruction[1])
        param_3_mode = int(instruction[0])
        if self._debug:
            print(instruction)
        if opcode == 1:
            # addition
            param_1 = self._read(self._instruction_pointer + 1)
            value_1 = self._get_value(param_1, param_1_mode)
            param_2 = self._read(self._instruction_pointer + 2)
            value_2 = self._get_value(param_2, param_2_mode)
            param_3 = self._read(self._instruction_pointer + 3)
            self._write(param_3, value_1 + value_2, param_3_mode)
            self._instruction_pointer += 4
        elif opcode == 2:
            # multiplicaiton
            param_1 = self._read(self._instruction_pointer + 1)
            value_1 = self._get_value(param_1, param_1_mode)
            param_2 = self._read(self._instruction_pointer + 2)
            value_2 = self._get_value(param_2, param_2_mode)
            param_3 = self._read(self._instruction_pointer + 3)
            self._write(param_3, value_1 * value_2, param_3_mode)
            self._instruction_pointer += 4
        elif opcode == 3:
            # input
            if len(self._inputs) == 0:
                self._inputs.append(-1)
            input_value = self._inputs.pop(0)
            store_address = self._read(self._instruction_pointer + 1)
            # print('  Store {0} at {1}, mode {2}'.format(input_value, store_address, param_1_mode))
            self._write(store_address, input_value, param_1_mode)
            self._instruction_pointer += 2
        elif opcode == 4:
            # output
            param_1 = self._read(self._instruction_pointer + 1)
            value_1 = self._get_value(param_1, param_1_mode)
            # print('  Output: read {0} from {1}'.format(value_1, param_1))
            self._outputs.append(value_1)
            self._instruction_pointer += 2
        elif opcode == 5:
            # jump if true
            param_1 = self._read(self._instruction_pointer + 1)
            value_1 = self._get_value(param_1, param_1_mode)
            param_2 = self._read(self._instruction_pointer + 2)
            value_2 = self._get_value(param_2, param_2_mode)
            if value_1 != 0:
                self._instruction_pointer = value_2
            else:
                self._instruction_pointer += 3
        elif opcode == 6:
            # jump if false
            param_1 = self._read(self._instruction_pointer + 1)
            value_1 = self._get_value(param_1, param_1_mode)
            param_2 = self._read(self._instruction_pointer + 2)
            value_2 = self._get_value(param_2, param_2_mode)
            if value_1 == 0:
                self._instruction_pointer = value_2
            else:
                self._instruction_pointer += 3
        elif opcode == 7:
            # less than
            param_1 = self._read(self._instruction_pointer + 1)
            value_1 = self._get_value(param_1, param_1_mode)
            param_2 = self._read(self._instruction_pointer + 2)
            value_2 = self._get_value(param_2, param_2_mode)
            param_3 = self._read(self._instruction_pointer + 3)
            if value_1 < value_2:
                self._write(param_3, 1, param_3_mode)
            else:
                self._write(param_3, 0, param_3_mode)
            self._instruction_pointer += 4
        elif opcode == 8:
            # equals
            param_1 = self._read(self._instruction_pointer + 1)
            value_1 = self._get_value(param_1, param_1_mode)
            param_2 = self._read(self._instruction_pointer + 2)
            value_2 = self._get_value(param_2, param_2_mode)
            param_3 = self._read(self._instruction_pointer + 3)
            if value_1 == value_2:
                self._write(param_3, 1, param_3_mode)
            else:
                self._write(param_3, 0, param_3_mode)
            self._instruction_pointer += 4
        elif opcode == 9:
            # equals
            param_1 = self._read(self._instruction_pointer + 1)
            value_1 = self._get_value(param_1, param_1_mode)
            self._relative_base += value_1
            self._instruction_pointer += 2
        elif opcode == 99:
            self._state = 'halt'
            return

    def run(self):
        # programme = self._programme
        self._state = 'run'
        while self._state != 'halt':
            instruction = '{0:05}'.format(self._read(self._instruction_pointer))
            opcode = int(instruction[-2:])
            param_1_mode = int(instruction[2])
            param_2_mode = int(instruction[1])
            param_3_mode = int(instruction[0])
            if self._debug:
                print(instruction)
            # print('{0}: op {1} p1m {2} p2m {3} p3m {4}'.format(
            #     instruction, opcode, param_1_mode, param_2_mode, param_3_mode))
            if opcode == 1:
                # addition
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                param_2 = self._read(self._instruction_pointer + 2)
                value_2 = self._get_value(param_2, param_2_mode)
                param_3 = self._read(self._instruction_pointer + 3)
                self._write(param_3, value_1 + value_2, param_3_mode)
                self._instruction_pointer += 4
            elif opcode == 2:
                # multiplicaiton
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                param_2 = self._read(self._instruction_pointer + 2)
                value_2 = self._get_value(param_2, param_2_mode)
                param_3 = self._read(self._instruction_pointer + 3)
                self._write(param_3, value_1 * value_2, param_3_mode)
                self._instruction_pointer += 4
            elif opcode == 3:
                # input
                if len(self._inputs) == 0:
                    self._state = 'wait'
                    return
                input_value = self._inputs.pop(0)
                store_address = self._read(self._instruction_pointer + 1)
                # print('  Store {0} at {1}, mode {2}'.format(input_value, store_address, param_1_mode))
                self._write(store_address, input_value, param_1_mode)
                self._instruction_pointer += 2
            elif opcode == 4:
                # output
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                # print('  Output: read {0} from {1}'.format(value_1, param_1))
                self._outputs.append(value_1)
                self._instruction_pointer += 2
            elif opcode == 5:
                # jump if true
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                param_2 = self._read(self._instruction_pointer + 2)
                value_2 = self._get_value(param_2, param_2_mode)
                if value_1 != 0:
                    self._instruction_pointer = value_2
                else:
                    self._instruction_pointer += 3
            elif opcode == 6:
                # jump if false
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                param_2 = self._read(self._instruction_pointer + 2)
                value_2 = self._get_value(param_2, param_2_mode)
                if value_1 == 0:
                    self._instruction_pointer = value_2
                else:
                    self._instruction_pointer += 3
            elif opcode == 7:
                # less than
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                param_2 = self._read(self._instruction_pointer + 2)
                value_2 = self._get_value(param_2, param_2_mode)
                param_3 = self._read(self._instruction_pointer + 3)
                if value_1 < value_2:
                    self._write(param_3, 1, param_3_mode)
                else:
                    self._write(param_3, 0, param_3_mode)
                self._instruction_pointer += 4
            elif opcode == 8:
                # equals
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                param_2 = self._read(self._instruction_pointer + 2)
                value_2 = self._get_value(param_2, param_2_mode)
                param_3 = self._read(self._instruction_pointer + 3)
                if value_1 == value_2:
                    self._write(param_3, 1, param_3_mode)
                else:
                    self._write(param_3, 0, param_3_mode)
                self._instruction_pointer += 4
            elif opcode == 9:
                # equals
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                self._relative_base += value_1
                self._instruction_pointer += 2
            elif opcode == 99:
                self._state = 'halt'
                return

    def _get_value(self, param, param_mode):
        if param_mode == 0:
            return self._read(param)
        elif param_mode == 1:
            return param
        elif param_mode == 2:
            return self._read(param + self._relative_base)

    def _read(self, address):
        if address not in self._memory.keys():
            self._write(address, 0)
        return self._memory[address]

    def _write(self, address, value, mode=1):
        if mode == 2:
            self._memory[address + self._relative_base] = value
        else:
            self._memory[address] = value

