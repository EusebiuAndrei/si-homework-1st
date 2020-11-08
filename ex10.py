def change_matrix(matrix):
    max_length = max([len(row) for row in matrix])
    new_matrix = [[matrix[0][j]] for j in range(0, max_length)]

    for i in range(1, len(matrix)):
        for j in range(0, len(matrix[i])):
            new_matrix[j].append(matrix[i][j])
        for j in range(len(matrix[i]) + 1, max_length):
            new_matrix[j].append(None)

    return new_matrix


if __name__ == '__main__':
    print(change_matrix([
        [1, 2, 3, 2, 1, 1],
        [2, 4, 4, 3, 7, 2],
        [5, 5, 2, 5, 6, 4],
        [6, 6, 7, 6, 7, 5]
    ]))
