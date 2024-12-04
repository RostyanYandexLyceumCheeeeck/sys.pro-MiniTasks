# https://leetcode.com/problems/dungeon-game/submissions/1470463370

from math import inf


def solution(arr):
    min_health = [[inf] * (len(arr[0]) + 1) for _ in range(len(arr) + 1)]
    min_health[-1][-2] = min_health[-2][-1] = 1

    for i in range(len(arr) - 1, -1, -1):
        for j in range(len(arr[0]) - 1, -1, -1):
            min_health[i][j] = max(1,
                                   min(min_health[i + 1][j],
                                       min_health[i][j + 1]
                                       ) - arr[i][j]
                                   )
    return min_health[0][0]


def test_1():
    arr = [[-2, -3, 3],
           [-5, -10, 1],
           [10, 30, -5]]
    # solution(arr)
    assert solution(arr) == 7


def test_2():
    arr = [[0, 0]]
    # solution(arr)
    assert solution(arr) == 1


def test_3():
    arr = [[-3, 5]]
    # solution(arr)
    assert solution(arr) == 4


def test_4():
    arr = [[3, -20, 30],
           [-3, 4, 0]]
    # solution(arr)
    assert solution(arr) == 1


def test_5():
    arr = [[1, -3, 3],
           [0, -2, 0],
           [-3, -3, -3]]
    # print(solution(arr))
    assert solution(arr) == 3


def test_6():
    arr = [[0, 0, 0],
           [-1, 0, 0],
           [2, 0, -2]]
    assert solution(arr) == 2


if __name__ == "__main__":
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
