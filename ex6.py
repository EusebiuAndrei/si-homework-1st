def get_numbers_with_frequency(frequency, *params):
    numbers = [number for numbers in params for number in numbers]
    return list(set([number for number in numbers if numbers.count(number) == frequency]))


if __name__ == '__main__':
    print(get_numbers_with_frequency(2, [1,2,3], [2,3,4],[4,5,6], [4,1, "test"]))
