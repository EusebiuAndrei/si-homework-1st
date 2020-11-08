import math
from typing import List, Tuple


def set_operations(A: List[int], B: List[int]) -> Tuple[List[int], List[int], List[int], List[int]]:
    intersection = [a for a in A for b in B if a == b]
    A_minus_B = [a for a in A if a in A and a not in B]
    B_minus_A = [b for b in B if b in B and b not in A]
    reunion = intersection + A_minus_B + B_minus_A

    return (intersection, reunion, A_minus_B, B_minus_A)


if __name__ == '__main__':
    A = [int(x) for x in list(input().split(' '))]
    B = [int(x) for x in list(input().split(' '))]
    result = set_operations(A, B)
    print(result[1])
