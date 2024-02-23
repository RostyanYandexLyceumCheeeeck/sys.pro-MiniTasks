import copy
import random
import itertools


def srav(x: list, y: list | None = None) -> bool:
    # print(x)
    # print(y)
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
        2:  [0, 2, 3, 4, 1, 5, 6, 7, 8],
        3: [0, 1, 5, 6, 2, 3, 4, 7, 8],
        4: [5, 1, 1, 2, 0, 0],
        5: [0, 1, 2, 3, 4, 5, 6, 7, 8],
        6: [5, 2, 3, 1],
    }
    for i in tests.keys():
        srav(tests[i])


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
    if not srav(three_copy, three):
        print("NOOOO333!")


def merge_ygl(arr: list[int], l: int, r: int, d1: int, d2: int, buffer: int):
    if not d1 or not d2:
        return

    d1 += l
    d2 += r

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


def app2(arr: list[int]):
    ost, t, l = 0, 1, len(arr)
    m = max(arr)

    while l > 1:
        t *= 2
        ost = max(ost, l % 2)
        l //= 2

    count = (t * 2 - len(arr))
    if ost:
        arr += [m] * count
        return count
    return 0


def ins(arr: list[int], l, r):
    while l + 1 < r and arr[l] > arr[l + 1]:
        arr[l], arr[l + 1] = arr[l + 1], arr[l]
        l += 1


def ygl(arr: list[int], l: int, r: int, step = 1):
    # print(f"{'  ' * step}{step})", arr[l:r], l, r)
    ln = r - l
    j = (l + r) // 2
    one, two = l, (l + j) // 2

    if ln < 2:
        return

    ygl(arr, two, j, step + 1)
    ygl(arr, l, two, step + 1)
    merge_ygl(arr, l, two, two - l, two - l, j)

    while j - l > 1:
        ygl(arr, l, two, step + 1)
        merge_ygl(arr, l, j, two - l, r - j, two)
        j = two
        two //= 2

    # print(f"{'  ' * step}{step})!", arr[one:r], l, r)
    ins(arr, l + 1, r)
    ins(arr, l, r)
    # print(f"{'  ' * step}{step})", arr[one:r], '\n')


def start_ygl(arr: list[int]):
    k = app2(arr)
    ygl(arr, 0, len(arr))
    if k:
        arr[:] = arr[:-k]
    return arr


def gg(arr: list[int], f, *args):
    print(arr)
    f(arr, *args)
    print(arr)


if __name__ == "__main__":
    debug = False
    if debug:
        z5 = [-74, 48, -20, 2, 10, -84, -5, -9, 11, -24, -91, 2, -71, 64, 63, 80, 28, -30, -58, -11, -44, -87, -22, 54,
              -74, -10, -55, -28, -46, 29, 10, 50, -72, 34, 26, 25, 8, 51, 13, 30, 35, -8, 50, 65, -6, 16, -2, 21, -78,
              35, -13, 14, 23, -3, 26, -90, 86, 25, -56, 91, -13, 92, -25, 37, 57, -20, -69, 98, 95, 45, 47, 29, 86,
              -28, 73, -44, -46, 65, -84, -96, -24, -12, 72, -68, 93, 57, 92, 52, -45, -2, 85, -63, 56, 55, 12, -85, 77,
              -39]
        gg(z5, start_ygl)
        print(srav(z5, sorted(z5)))
    else:
        base_test()
        test1()
        test2()
