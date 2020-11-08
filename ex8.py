def filter_strings(strings, value = 1, divisible = True):
    filtered_strings = []
    for my_string in strings:
        if divisible:
            filtered_strings.append(list(filter(lambda e: ord(e) % value == 0, my_string)))
        else:
            filtered_strings.append(list(filter(lambda e: ord(e) % value != 0, my_string)))

    return filtered_strings


if __name__ == '__main__':
    print(filter_strings(["test", "hello", "lab002"], 2, False))