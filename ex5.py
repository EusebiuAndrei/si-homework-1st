def fill_0(matrix):
    for i, j in [[i, j] for i in range(len(matrix)) for j in range(len(matrix[i])) if i > j]:
        matrix[i][j] = 0
    return matrix


if __name__ == '__main__':
    matrix = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]]
    print(fill_0(matrix))
