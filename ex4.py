def get_song(notes, moves, start):
    return [notes[(start + move) % len(notes)] for move in moves]


if __name__ == '__main__':
    # notes = [x for x in list(input().split(' '))]
    # moves = [int(x) for x in list(input().split(' '))]
    # start = int(input())
    print(get_song(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2))
