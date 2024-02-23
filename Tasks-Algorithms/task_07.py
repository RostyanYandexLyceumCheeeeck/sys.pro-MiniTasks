# https://leetcode.com/problems/sort-an-array/submissions/1184336454
import copy
import random
import itertools


def srav(x: list, y: list | None = None) -> bool:
    if y is None:
        y = sorted(x)
    if len(x) != len(y):
        return False

    for i in range(len(x)):
        if x[i] != y[i]:
            return False
    return True


def base_test():
    tests = {
        0: [6, 7, 8, 9, 10, 11, 1, 2, 3, 4, 5, 12],
        1: [1, 2, 4, 8, 9, 10, 3, 5, 6, 7, 11, 12],
        2: [0, 2, 3, 4, 1, 5, 6, 7, 8],
        3: [0, 1, 5, 6, 2, 3, 4, 7, 8],
        4: [5, 1, 1, 2, 0, 0],
        5: [0, 1, 2, 3, 4, 5, 6, 7, 8],
        6: [5, 2, 3, 1],
        7: [-1, -7, 4],
        8: [-74, 48, -20, 2, 10, -84, -5, -9, 11, -24, -91, 2, -71, 64, 63, 80, 28, -30, -58, -11, -44, -87, -22, 54,
            -74, -10, -55, -28, -46, 29, 10, 50, -72, 34, 26, 25, 8, 51, 13, 30, 35, -8, 50, 65, -6, 16, -2, 21, -78,
            35, -13, 14, 23, -3, 26, -90, 86, 25, -56, 91, -13, 92, -25, 37, 57, -20, -69, 98, 95, 45, 47, 29, 86, -28,
            73, -44, -46, 65, -84, -96, -24, -12, 72, -68, 93, 57, 92, 52, -45, -2, 85, -63, 56, 55, 12, -85, 77, -39]
    }
    for i in tests.keys():
        start_ygl(tests[i])
        if not srav(tests[i]):
            print("AAAA", i)


def test1():
    arr = [x for x in range(9)]
    g = 0
    for data in itertools.permutations(arr):
        mas = list(data)
        c_mas = copy.copy(mas)
        g += 1
        start_ygl(mas)
        if not srav(arr, mas):
            print("BAD!!!")
            print(g, mas)
            print(g, c_mas)
            print(g, arr)
            break
    else:
        print("YEP!!!")


def test2():
    one = [x for x in range(10 ** 4)]
    two = [x for x in range(10 ** 6)]
    three = copy.copy(one) * 4

    one_copy = copy.copy(one)
    two_copy = copy.copy(two)
    three_copy = copy.copy(three)

    random.shuffle(one_copy)
    random.shuffle(two_copy)
    random.shuffle(three_copy)

    start_ygl(one_copy)
    start_ygl(two_copy)
    start_ygl(three_copy)

    if not srav(one_copy, one):
        print("NOOOO111!")
    if not srav(two_copy, two):
        print("NOOOO222!")
    if not srav(three_copy):
        print("NOOOO333!")


def merge_ygl(arr: list[int], l: int, r: int, d1: int, d2: int, buffer: int):
    if not d1 or not d2:
        return

    while l < d1 and r < d2:
        if arr[r] < arr[l]:
            arr[r], arr[buffer] = arr[buffer], arr[r]
            r += 1
        else:
            arr[l], arr[buffer] = arr[buffer], arr[l]
            l += 1
        buffer += 1

    while l < d1:
        arr[l], arr[buffer] = arr[buffer], arr[l]
        l += 1
        buffer += 1

    while r < d2:
        arr[r], arr[buffer] = arr[buffer], arr[r]
        r += 1
        buffer += 1


def ins(arr: list[int], l, r):
    while l + 1 < r and arr[l] > arr[l + 1]:
        arr[l], arr[l + 1] = arr[l + 1], arr[l]
        l += 1


def ygl(arr: list[int], l: int, r: int):
    ln = r - l
    if ln < 2:
        return
    if ln < 4:
        for i in range(l + ln - 2, l - 1, -1):
            ins(arr, i, r)
        return

    st = l
    l += ln % 4
    j = (l + r) // 2
    two = (l + j) // 2

    ygl(arr, l, two)
    ygl(arr, two, j)
    merge_ygl(arr, l, two, two, j, j)

    while two - l > 1:
        ygl(arr, l, two)
        merge_ygl(arr, l, j, two, r, two)
        j = two + (two - l) % 2
        two = (l + j) // 2

    for i in range(j - 1, st - 1, -1):
        ins(arr, i, r)


def start_ygl(arr: list[int]):
    ygl(arr, 0, len(arr))
    return arr


def gg(arr: list[int], f, *args):
    print(arr)
    f(arr, *args)
    print(arr)
    print(srav(arr))


if __name__ == "__main__":
    debug = False
    if debug:
        z5 = [-74, 48, -20, 2, 10, -84, -5, -9, 11, -24, -91, 2, -71, 64, 63, 80, 28, -30, -58, -11, -44, -87, -22, 54,
              -74, -10, -55, -28, -46, 29, 10, 50, -72, 34, 26, 25, 8, 51, 13, 30, 35, -8, 50, 65, -6, 16, -2, 21, -78,
              35, -13, 14, 23, -3, 26, -90, 86, 25, -56, 91, -13, 92, -25, 37, 57, -20, -69, 98, 95, 45, 47, 29, 86,
              -28, 73, -44, -46, 65, -84, -96, -24, -12, 72, -68, 93, 57, 92, 52, -45, -2, 85, -63, 56, 55, 12, -85, 77,
              -39]
        gg(z5, start_ygl)
    else:
        base_test()
        test1()
        test2()
