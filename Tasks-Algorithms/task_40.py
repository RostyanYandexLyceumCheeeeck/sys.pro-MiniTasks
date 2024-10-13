# https://leetcode.com/problems/minimum-cost-to-merge-stones/submissions/1421395933


import math

debug = True


def decomposition_sum(arr: list[list[int]], i: int, j: int, end_j: int, step, k) -> int:
    # print("   " * (step - k + 1) + f"INIT {i, j, end_j} ({step, k})")
    if k == 1:
        return arr[i][end_j] if i != end_j else 0

    res = math.inf
    for x in range(j, end_j, step):
        # print("   " * (step - k + 1) + f"STEP {x} ({x - i + 1, x})")
        q = decomposition_sum(arr, x + 1, x + 1, end_j, step, k - 1)
        q += arr[i][x] if i != x else 0
        res = min(res, q)

    return res


def solution2(arr, step):
    step -= 1
    n = len(arr)

    if n == 1:
        return 0

    if (n - 1) % step:
        return -1

    prefix_sum = [arr[0]]

    for i in range(1, n):
        prefix_sum.append(prefix_sum[-1] + arr[i])

    ####################
    if debug:
        print(prefix_sum)
    ####################

    table = [[0] * n for _ in range(n)]

    for i in range(n):
        table[i][i] = arr[i]

    for i in range(n - step):
        table[i][i + step] = prefix_sum[i + step] - prefix_sum[i] + arr[i]

    for l in range(2 * step, n, step):
        for i in range(n - l):
            j = i + l

            w = prefix_sum[j] - prefix_sum[i] + arr[i]

            ####################
            if debug:
                print(i, j, w)
            ####################

            table[i][j] = w + decomposition_sum(table, i, i, j, step, step + 1)

    ################################################################
    if debug:
        asd = max(map(str, table[-1]), key=len)
        # for i in table:
        #     for j in i:
        #         print(str(j).center(len(asd), ' '), end='\t')
        #     print()
        print(*table, sep='\n')
    ################################################################

    return table[0][-1] if table[0][-1] else -1


def test_0():
    arr = [1, 18, 23, 3, 8, 15, 2]
    step = 3
    assert solution2(arr, step) == 137


def test_1():
    arr = [3, 2, 4, 1]
    step = 2
    assert solution2(arr, step) == 20


def test_2():
    arr = [3, 5, 1, 2, 6]
    step = 3
    assert solution2(arr, step) == 25


def test_3():
    arr = [7, 7, 8, 6, 5, 6, 6]
    step = 3
    assert solution2(arr, step) == 83


def test_4():
    arr = [7, 7, 8, 6, 5, 6, 6, 7, 6]
    step = 3
    assert solution2(arr, step) == 116


def test_5():
    arr = [7, 7, 8, 6, 5, 6, 6, 7, 6, 3, 9]
    step = 3
    assert solution2(arr, step) == 156


def test_6():
    arr = [4, 6, 4, 7, 5]
    step = 2
    assert solution2(arr, step) == 62


if __name__ == "__main__":
    test_0()
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
