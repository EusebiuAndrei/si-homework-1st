def who_cannot_watch_game(matrix):
    people = []
    for i in range(1, len(matrix)):
        for j in range(0, len(matrix[i])):
            tallest = max([matrix[x][j] for x in range(0, i)])
            if matrix[i][j] <= tallest:
                people.append((i, j))

    return people


if __name__ == '__main__':
    print(who_cannot_watch_game([
        [1, 2, 3, 2, 1, 1],
        [2, 4, 4, 3, 7, 2],
        [5, 5, 2, 5, 6, 4],
        [6, 6, 7, 6, 7, 5]
    ]))
