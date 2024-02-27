# https://leetcode.com/problems/sort-colors/submissions/1188089877
from random import randint

factory = lambda x: [randint(0, 2) for _ in range(x)]


def test1():
    for _ in range(100):
        size = randint(0, 10**5)
        one = factory(size)
        assert nederland(one) == sorted(one)


def nederland(arr: list[int]):
    if len(arr) < 2:
        return arr

    target = 1
    c, k = 0, 0  # counters 0 and 1
    for i in range(len(arr)):
        if arr[i] < target:
            arr[c + k], arr[i], arr[c] = arr[c], arr[c + k] if c + k != i else arr[c], arr[i]
            c += 1
        elif arr[i] == target:
            arr[i], arr[c + k] = arr[c + k], arr[i]
            k += 1

    return arr


if __name__ == "__main__":
    test1()
