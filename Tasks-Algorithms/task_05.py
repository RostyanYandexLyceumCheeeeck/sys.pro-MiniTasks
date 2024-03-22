# https://leetcode.com/problems/h-index/submissions/1195888553
from random import randint, shuffle
from copy import copy


def cache(func):
    four = {0: 0,
            1: 4}

    def posrednik(arr: list[int], l: int = 0, r: int | None = None, k: int = 0, step: int = 0):
        if k not in four:
            four[k] = four[k - 1] * 4
        step = four[k // 2]
        if not (k % 2):
            step //= 2
        if k == 1:
            step = 1

        step *= 3
        step += four[k] + 1
        return func(arr, l, r, k, step)
    return posrednik


def control(func):
    def posrednik(arr: list[int], l: int = 0, r: int | None = None, k: int = 0, step: int = 0):
        if not r:
            r = len(arr)

        if (r - l) < 2 or len(arr) < 2:
            return arr
        return func(arr, l, r, k, step)
    return posrednik


@cache
@control
def recurs_shellsort(arr: list[int], l: int = 0, r: int | None = None, k: int = 0, step: int = 0):
    if step < (r - l):
        recurs_shellsort(arr, l, r, k + 1, step)

    for i in range(l + step, r):
        target, j = arr[i], i
        while j - step > -1 and arr[j - step] > target:
            arr[j] = arr[j - step]
            j -= step
        arr[j] = target


def hIndex(citations: list[int]) -> int:
    recurs_shellsort(citations)
    r = len(citations)
    while r and len(citations) - r + 1 <= citations[r - 1]:
        r -= 1
    return len(citations) - r


def test1_sort():
    count = randint(10**2, 10**5)

    for _ in range(count):
        mas = [x for x in range(randint(0, 10**3))]
        c_mas = copy(mas)
        shuffle(c_mas)
        recurs_shellsort(c_mas)
        assert c_mas == mas


def base_test_hindex():
    one = [3, 0, 6, 1, 5]
    two = [1, 3, 1]
    three = [100]
    print(hIndex(one))
    print(hIndex(two))
    print(hIndex(three))


if __name__ == "__main__":
    # test1_sort()
    base_test_hindex()
