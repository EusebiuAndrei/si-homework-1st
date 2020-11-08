def get_fib_array(n):
    if n <= 0:
        return []
    elif n == 1:
        return [1]

    fib = [1, 1]
    for i in range(2, n):
        fib.append(fib[i - 2] + fib[i - 1])

    return fib


if __name__ == '__main__':
    n = int(input())
    print(get_fib_array(n))
