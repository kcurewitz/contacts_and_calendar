import sys
import operator
from functools import reduce
from itertools import accumulate

total_calculations = 0
goals = [2025, 2026, 2027]

def calculate_permutations(operands):
    # operation represented by 8 2-bit numbers, 2 bits = 4 operation codes
    # 00 00 00 00 00 00 00 00
    # 00 00 00 00 00 00 00 01
    global total_calculations

    operators = [" + ", " - ", " * ", " / "]
    op_bits = 2*(len(operands) - 1)                 # one operator between operands
    for operations in range(0,2**(op_bits)):        # permutations of operators
        equation = operands[0]
        for place in range(0,len(operands)-1):      # build the equation
            op_index = (operations >> (place*2)) & 0x3
            equation += operators[op_index]
            equation += str(operands[place+1])

        answer = eval(equation)                     # calculate
        total_calculations += 1

        if answer in goals:                         # compare to goals
            print(int(answer), " = ", equation)
    return
        
# return digits split into all permutations of sizes from 1 to total number of digits in string
def split_digits(digit_string, strides):
    place = 0
    i = 0
    operands = list()
    while (place < len(digit_string)):
        operands.append(digit_string[place:(place+strides[i])])
        place = place+strides[i]
        i += 1
    return operands
    
def permute_and_solve(digit_string = "1"):
    import itertools
    strides = list(itertools.product(list(range(1,5)), repeat=len(digit_string)))
    digit_string_len = len(digit_string)
    last_strides = list()
    for stride in strides:
        s = list(stride)
        a_s = list(accumulate(s,operator.add))
        if digit_string_len in a_s:      # only use strides adding up to string length
            i = a_s.index(digit_string_len)
            # check for consecutive duplicates and only use first instance
            # this check *might* not work if permutations are not sorted?
            if last_strides != a_s[0:i+1]:
                numbers = split_digits(digit_string,s)
                calculate_permutations(numbers)
                last_strides = a_s[0:i+1]
    print("Total calculations: ", total_calculations)
    return

def main() -> int:
    #https://www.npr.org/2026/01/11/g-s1-104903/sunday-puzzle
    print("="*10," NPR answers for 2026:")
    print("1 + 2 + 345 × 6 - 7 × 8 + 9")
    print("12 × 34 × 5 - 6 - 7 + 8 - 9")
    print("="*10," Our answers")
    digit_string = "123456789"
    permute_and_solve(digit_string)
    sys.stdout.flush()
    return 0

__name__ == '__main__'
debug = 0
if debug > 0: print("recursion limit: ", sys.getrecursionlimit())
sys.exit(main())