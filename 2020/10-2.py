import argparse
import os


def main():
    day = os.path.basename(__file__).split('-')[0]
    challenge_input = '{}-input.txt'.format(day)
    challenge_input = '{}-example-1.txt'.format(day)
    # challenge_input = '{}-example-2.txt'.format(day)

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=challenge_input)
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    numbers = []
    for line in lines:
        numbers.append(int(line))

    sorted_numbers = sorted(numbers)
    sorted_numbers.append(sorted_numbers[-1] + 3)
    runs_of_ones = []

    """
    1    2    3    4    5    6    7
    
    1 +- 2                                        
      +------ 3                                   
      +----------- 4                              
         2 +- 3
           +------ 4
           +----------- 5
              3 +- 4
                +------ 5
                +----------- 6
                   4 +- 5
                     +------ 6
                     +----------- 7
                        5 +- 6
                          +------ 7
                             6 +- 7

    ways in:   1>     1>     2>     3>     3>     3>     3>              
    position:    1      2      3      4      5      6      7
    ways out:     >3     >3     >3     >3     >2     >1     >1

    ways in * ways out ?
    
    
    4 5 6
    
    4, 5, 6
    4,    6
    
    = 2
    
    
    4  5  6  7
    output:   4 5 6 7
    ways in:  1 1 2 3
    ways out: 3 2 1 1
    4 = 2*2 - 0
    
    4, 5, 6, 7
    4, 5,    7
    4,    6, 7
    4,       7
    
    
    4  5  6  7  8
    output:   4 5 6 7 8
    ways in:  1 1 2 3 3
    ways out: 3 3 2 1 1
    7 = 2*3 + 1  or  2^3 - 1
    
    4, 5, 6, 7, 8
    4, 5, 6,    8
    4, 5,    7, 8
    4, 5,       8
    4,    6, 7, 8
    4,    6,    8
    4,       7, 8
    
    
    4  5  6  7  8  9
    output:   4 5 6 7 8 9
    ways in:  1 1 2 3 3 3
    ways out: 3 3 3 2 1 1
    13 = 7*2 - 1 or 4*3 + 1  |  2^4 - 3
    
    4, 5, 6, 7, 8, 9
    4, 5, 6, 7,    9
    4, 5, 6,    8  9
    4, 5, 6,       9
    4, 5,    7, 8, 9
    4, 5,    7,    9
    4, 5,       8, 9
    4,    6, 7, 8, 9
    4,    6, 7,    9
    4,    6,    8  9
    4,    6,       9
    4,       7, 8, 9
    4,       7,    9
    
    
    24 = 13*2 - 2 or 7*3 + 3 or 2^3  or 6*3 + 6 
       = 2^5 - 8
    
    4  5  6  7  8  9  10
    
    4, 5, 6, 7, 8, 9, 10
    4, 5, 6, 7, 8,    10
    4, 5, 6, 7,    9, 10
    4, 5, 6, 7,       10
    4, 5, 6,    8, 9, 10
    4, 5, 6,    8,    10
    4, 5, 6,       9, 10
    4, 5,    7, 8, 9, 10
    4, 5,    7, 8,    10
    4, 5,    7,    9, 10
    4, 5,    7,       10
    4, 5,       8, 9, 10
    4, 5,       8,    10
    4,    6, 7, 8, 9, 10
    4,    6, 7, 8,    10
    4,    6, 7,    9, 10
    4,    6, 7,       10
    4,    6,    8, 9, 10
    4,    6,    8,    10
    4,    6,       9, 10
    4,       7, 8, 9, 10
    4,       7, 8,    10
    4,       7,    9, 10
    4,       7,       10
    
    """

    output = 0
    last_difference = -1
    for number in sorted_numbers:
        difference = number - output
        if difference == 1:
            if last_difference == 1:
                runs_of_ones[-1] += 1
            else:
                runs_of_ones.append(1)
        last_difference = difference

        print('{} -> {} = {}'.format(output, number, difference))
        output = number

    print(runs_of_ones)

    paths = 1
    for run_of_ones in runs_of_ones:
        if run_of_ones == 2:
            paths += 1
        elif run_of_ones > 2:
            paths += run_of_ones * 2 - 3

    print('paths:', paths)


if __name__ == "__main__":
    main()
