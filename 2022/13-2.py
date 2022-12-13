from aocutils import load_input
from functools import cmp_to_key

from input_13 import get_pairs
# from example_13 import get_pairs

def main():

    def cmp(left, right) -> int:
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return -1
            if right < left:
                return 1
            return 0
        if isinstance(left, list) and isinstance(right, list):
            left_len = len(left)
            right_len = len(right)
            common_length = min(left_len, right_len)
            for index in range(common_length):
                comparison = cmp(left[index], right[index])
                if comparison != 0:
                    return comparison
            return cmp(left_len, right_len)
        if isinstance(left, int):
            return cmp([left], right)
        if isinstance(right, int):
            return cmp(left, [right])
    
    all_packets:list = []

    for pair_index, (left, right) in enumerate(get_pairs(), start=1):
        all_packets += [left, right]
    
    divider_1 = [[2]]
    divider_2 = [[6]]
    all_packets.append(divider_1)
    all_packets.append(divider_2)
    
    all_packets.sort(key=cmp_to_key(cmp))

    div_1_index = all_packets.index(divider_1) + 1
    div_2_index = all_packets.index(divider_2) + 1

    print(div_1_index * div_2_index)

    # Correct answer: 20758


if __name__ == "__main__":
    main()
