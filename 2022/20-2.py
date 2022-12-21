from aocutils import load_input


def main():

    class Number():
        def __init__(self, number:int, intitial_position:int) -> None:
            self.original_val:int = number

            moves_per_loop = len(puzzle_input) - 1
            if number >= 0:
                self.val:int = min(number, moves_per_loop + number % moves_per_loop)
            else:
                self.val:int = max(number, moves_per_loop + number % -moves_per_loop)

            self.start_pos:int = intitial_position
            self.pos:int = intitial_position
            self.prev = None
            self.next = None
        
        def __eq__(self, __o: object) -> bool:
            return self.val == __o.val and self.start_pos == __o.start_pos
        
        def __str__(self) -> str:
            return f'{self.val}'

        def __repr__(self) -> str:
            return self.__str__()


    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    initial:list[Number] = []
    zero:Number = None

    for i, number in enumerate(puzzle_input):
        val = int(number) * 811_589_153
        number = Number(val, i)
        if val == 0:
            zero = number
        initial.append(number)

    count = len(initial)

    for i, number in enumerate(initial):
        number.prev = initial[(i - 1) % count]
        number.next = initial[(i + 1) % count]

    print(initial)
    mixed:dict[int,Number] = { number.pos:number for number in initial }
    for number in sorted(mixed):
        print(mixed[number].original_val, end=', ')
    print()
    for number in sorted(mixed):
        print(mixed[number].val, end=', ')
    print()

    for mix in range(10):
        print('Mix', mix)
        for number in initial:
            for _ in range(abs(number.val)):
                number_pos:int = number.pos
                left:Number = number.prev
                right:Number = number.next
                if number.val >= 0:
                    right_pos:int = right.pos
                    left.next = right
                    right.prev = left
                    number.prev = right
                    number.next = right.next
                    number.next.prev = number
                    right.next = number
                    right.pos = number_pos
                    number.pos = right_pos
                elif number.val < 0:
                    left_pos:int = left.pos
                    right.prev = left
                    left.next = right
                    number.next = left
                    number.prev = left.prev
                    left.prev = number
                    number.prev.next = number
                    left.pos = number_pos
                    number.pos = left_pos

        mixed:dict[int,Number] = { number.pos:number for number in initial }
        # for number in sorted(mixed):
        #     print(mixed[number].original_val, end=', ')
        # print()

    pos_0 = zero.pos
    print('pos 0', pos_0)
    num_1 = mixed[(pos_0 + 1000) % count]
    num_2 = mixed[(pos_0 + 2000) % count]
    num_3 = mixed[(pos_0 + 3000) % count]
    print(num_1.original_val, num_2.original_val, num_3.original_val)
    print('sum', num_1.original_val + num_2.original_val + num_3.original_val)

    # Correct answer: 14579387544492


if __name__ == "__main__":
    main()
