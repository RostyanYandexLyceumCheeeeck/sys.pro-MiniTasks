# lomuto --> https://leetcode.com/problems/sort-an-array/submissions/1189706468
# hoara --> https://leetcode.com/problems/sort-an-array/submissions/1189822706

from random import randint, shuffle
from copy import copy
from time import time


def check(arr, func):
    first = copy(arr)
    second = sorted(arr)
    flag = func(arr) == second

    if not flag:
        print(first)
        print(arr)
        print(second)
    assert flag


def base_tests(func, multiplier: int = 1):
    one = [x for x in range(3)] * multiplier
    two = one[::-1]
    three = copy(one)
    shuffle(three)

    check(one, func)
    check(two, func)
    check(three, func)


def test1():
    size = randint(100, 1000)
    count = randint(10, 100)
    print(f"{size = }, {count = }")

    mas = [x for x in range(size)] * 4
    answer = sorted(mas)
    for _ in range(count):
        shuffle(mas)
        new_mas = copy(mas)
        assert lomuto_quick_sort(mas) == hoare_quick_sort(new_mas) == answer


def control(func):
    def posrednik(arr: list[int], start: int = 0, end: int | None = None):
        if len(arr) < 2:
            return arr

        if end is None:
            end = len(arr)

        if end - start < 2:
            return arr
        return func(arr, start, end)
    return posrednik


@control
def lomuto_quick_sort(arr: list[int], start: int = 0, end: int = 0):
    temp = randint(start, end - 1)
    target = arr[temp]
    arr[temp], arr[start] = arr[start], arr[temp]
    i, k = start, start

    for j in range(start + 1, end):
        if arr[j] < target:
            arr[j], arr[k + 1], arr[i] = arr[k + 1], arr[i], arr[j]
            i += 1
            k += 1
        elif arr[j] == target:
            arr[k + 1], arr[j] = arr[j], arr[k + 1]
            k += 1

    lomuto_quick_sort(arr, start, i)
    lomuto_quick_sort(arr, k + 1, end)
    return arr


@control
def hoare_quick_sort(arr: list[int], start: int = 0, end: int = 0):
    ln = (end - start) // 4
    temp = randint(start + ln, end - 1 - ln)
    target = arr[temp]
    l, r = start, end - 1

    while l < r:
        if arr[l] <= target and l < temp:
            l += 1
            continue
        if arr[r] > target and r > temp:
            r -= 1
            continue
        if arr[l] != target or arr[r] != target:
            flag = False

        arr[l], arr[r] = arr[r], arr[l]
        if l == temp:
            temp = r
        elif r == temp:
            temp = l

    hoare_quick_sort(arr, start, temp)
    hoare_quick_sort(arr, temp, end)

    return arr


def tt():
    qwe = [2] * 10**6
    s = time()
    hoare_quick_sort(qwe)
    print(time() - s)


if __name__ == "__main__":
    # base_tests(lomuto_quick_sort)
    # base_tests(hoare_quick_sort)
    # base_tests(lomuto_quick_sort, 5)
    # base_tests(hoare_quick_sort, 5)
    # test1()
    tt()
