from random import randint
from copy import copy

factory = lambda x, y: ["".join([chr(randint(65, 88)) for _ in range(x)]) for _ in range(y)]


def base_test():
    one = ["qwert", "asdfg", "aadfg", "zxccv", "zxccv", "rtyyq"]

    assert LSD_sort(one) == sorted(one)


def test1():
    m_t = {
        0: factory(1, 100),
        1: factory(100, 1),
        2: factory(2, 50),
        3: factory(20, 1000),
    }
    for i in m_t.keys():
        one = copy(m_t[i])
        assert LSD_sort(one) == sorted(one)


def support(arr: list[str], ind):
    res = [0] * len(arr)
    count = [0] * 256

    for s in arr:
        count[ord(s[ind])] += 1

    for i in range(len(count) - 1):
        count[i + 1] += count[i]

    for j in range(-1, -len(arr) - 1, -1):
        res[count[ord(arr[j][ind])] - 1] = arr[j]
        count[ord(arr[j][ind])] -= 1

    return res


def LSD_sort(arr: list[str]):
    for ind in range(len(arr[0]) - 1, -1, -1):
        arr = support(arr, ind)
    return arr


if __name__ == "__main__":
    base_test()
    test1()
