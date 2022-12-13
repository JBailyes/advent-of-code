from aocutils import load_input

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
            
    sum = 0
    for pair_index, (left, right) in enumerate(get_pairs(), start=1):
        correct = cmp(left, right) == -1
        if correct:
            sum += pair_index
    print(sum)

    # Correct answer: 6070


if __name__ == "__main__":
    main()
