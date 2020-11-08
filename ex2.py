import math
from typing import List


def get_prime_numbers(numbers: List[int]) -> List[int]:
    return [x for x in numbers if len([y for y in range(2, math.floor(x ** 0.5) + 1) if x % y == 0]) == 0]


if __name__ == '__main__':
    numbers = [int(x) for x in list(input().split(' '))]
    print(get_prime_numbers(numbers))
