# https://leetcode.com/problems/create-sorted-array-through-instructions/submissions/1470498845

ABSOLUTE = 10 ** 9 + 7


def f(x):
    return x & (x + 1)


def g(x):
    return x | (x + 1)


class FenwickTree:
    def __init__(self, size):
        self.arr: list = [0] * size

    def prefix_sum(self, curr_pos):
        res = 0
        while curr_pos >= 0:
            res += self.arr[curr_pos]
            curr_pos = f(curr_pos) - 1
        return res

    def sum_range(self, start, end):
        return self.prefix_sum(end) - self.prefix_sum(start)

    def increment(self, pos):
        while pos < len(self.arr):
            self.arr[pos] += 1
            pos = g(pos)


def test(arr, ans):
    size = max(arr)
    ft = FenwickTree(size)
    res = 0

    for x in arr:
        x -= 1
        res += min(ft.prefix_sum(x - 1), ft.sum_range(x, size - 1))
        res %= ABSOLUTE
        ft.increment(x)

    assert res == ans


def test_1():
    test([1, 5, 6, 2], 1)


def test_2():
    test([2, 3, 4, 7, 6, 5, 1, 1], 3)


def test_3():
    test([1, 3, 3, 3, 2, 4, 2, 1, 2], 4)


if __name__ == "__main__":
    test_1()
    test_2()
    test_3()
