def is_palindrome(x):
    return str(x)[::-1] == str(x)


def palindromes_tuples(numbers):
    palindromes = [number for number in numbers if is_palindrome(number) is True]
    return len(palindromes), max(palindromes)


if __name__ == '__main__':
    print(palindromes_tuples([1, 22, 395, 101]))
