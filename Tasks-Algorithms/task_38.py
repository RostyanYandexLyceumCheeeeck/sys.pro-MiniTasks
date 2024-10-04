# https://leetcode.com/problems/dungeon-game/submissions/1411473160

from copy import deepcopy


def step(arr, heart, bot_heart, from_: tuple[int, int], to: tuple[int, int]):
    x, y = from_
    i, j = to
    save = arr[i][j]

    if save >= 0:
        heart[i][j] = heart[x][y] + save
        bot_heart[i][j] = bot_heart[x][y]
    elif heart[x][y] <= abs(save):
        delta = abs(save) - heart[x][y]
        heart[i][j] = 1
        bot_heart[i][j] = bot_heart[x][y] + delta + 1
    else:
        heart[i][j] = heart[x][y] + save
        bot_heart[i][j] = bot_heart[x][y]

    return bot_heart[i][j], heart[i][j]


def solution(arr, heart=None, bot_heart=None):
    n, m = len(arr), len(arr[0])

    # heart = [[0] * m for _ in range(n)]
    heart[0][0] = 1 if arr[0][0] < 0 else (arr[0][0] + 1)
    # bot_heart = deepcopy(heart)  # minimal heart
    bot_heart[0][0] = abs(arr[0][0] - 1) if arr[0][0] < 0 else 1

    for j in range(1, m):
        step(arr, heart, bot_heart, (0, j - 1), (0, j))

    for i in range(1, n):
        step(arr, heart, bot_heart, (i - 1, 0), (i, 0))

    # print("====== ARR ======", *arr, sep='\n', end='\n\n')
    # print("===== HEART =====", *heart, sep='\n', end='\n\n')
    # print("=== BOT_HEART ===", *bot_heart, sep='\n', end='\n\n')

    for i in range(1, n):
        for j in range(1, m):
            up = step(arr, heart, bot_heart, (i - 1, j), (i, j))
            left = step(arr, heart, bot_heart, (i, j - 1), (i, j))

            if left[0] < up[0] or (left[0] == up[0] and left[1] >= up[1]):
                # print('left')
                continue
            else:
                step(arr, heart, bot_heart, (i - 1, j), (i, j))
    #             print('up')
    # print("===========================\n")
    # print("====== ARR ======", *arr, sep='\n', end='\n\n')
    # print("===== HEART =====", *heart, sep='\n', end='\n\n')
    # print("=== BOT_HEART ===", *bot_heart, sep='\n', end='\n\n')

    return bot_heart[-1][-1]


def bin_search_solution(arr):
    n, m = len(arr), len(arr[0])

    heart = [[0] * m for _ in range(n)]
    heart[0][0] = 1 if arr[0][0] < 0 else (arr[0][0] + 1)
    bot_heart = deepcopy(heart)  # minimal heart
    bot_heart[0][0] = abs(arr[0][0] - 1) if arr[0][0] < 0 else 1

    left, right = 0, solution(arr, heart, bot_heart)
    save = right

    while left < right - 1:
        middle = (right + left) // 2

        arr[0][0] += middle
        new_val = solution(arr, heart, bot_heart)
        arr[0][0] -= middle

        # print(left, right, new_val)
        if new_val == 1:
            right = middle
            continue
        left = middle
        save = min(save, new_val + middle)

    # print(right)
    # print(save)
    return min(save, right + 1)


def test_1():
    arr = [[-2, -3, 3],
           [-5, -10, 1],
           [10, 30, -5]]
    # solution(arr)
    assert bin_search_solution(arr) == 7


def test_2():
    arr = [[0, 0]]
    # solution(arr)
    assert bin_search_solution(arr) == 1


def test_3():
    arr = [[-3, 5]]
    # solution(arr)
    assert bin_search_solution(arr) == 4


def test_4():
    arr = [[3, -20, 30],
           [-3, 4, 0]]
    # solution(arr)
    assert bin_search_solution(arr) == 1


def test_5():
    arr = [[1, -3, 3],
           [0, -2, 0],
           [-3, -3, -3]]
    # print(solution(arr))
    assert bin_search_solution(arr) == 3


def test_6():
    arr = [[0, 0, 0],
           [-1, 0, 0],
           [2, 0, -2]]
    assert bin_search_solution(arr) == 2


if __name__ == "__main__":
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
