def my_sort(list_of_tuples):
    return sorted(list_of_tuples, key=lambda e: e[1][2])


if __name__ == '__main__':
    print(my_sort([('abc', 'bcd'), ('abc', 'zza')]))
