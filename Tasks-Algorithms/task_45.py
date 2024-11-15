# https://leetcode.com/problems/create-sorted-array-through-instructions/submissions/1453054070


from bisect import bisect_left, bisect_right


def f(x):
    return x & (x + 1)


def g(x):
    return x | (x + 1)


class FenwickTree:
    def __init__(self, arr):
        self.arr: list[list] = []
        self.build_init(arr)

    def build_init(self, arr):
        self.arr = [sorted(arr[f(i):i + 1]) for i in range(len(arr))]

    def get_index(self, pos, value, func):
        res = 0
        curr_pos = pos
        while curr_pos >= 0:
            target_arr = self.arr[curr_pos]
            # res += min(bisect_left(target_arr, value),
            #            len(target_arr) - bisect_right(target_arr, value))
            res += func(target_arr, value)
            curr_pos = f(curr_pos) - 1
        return res

    def sum(self, pos, value):
        return min(
            self.get_index(pos, value, bisect_left),
            self.get_index(pos, value, lambda mas, x: len(mas) - bisect_right(mas, x))
        )


def test(arr, ans):
    ft = FenwickTree(arr)
    res = 0

    for i in range(len(arr)):
        res += ft.sum(i, arr[i])
    res %= 10 ** 9 + 7
    # print(res)
    assert res == ans


def test_1():
    test([1, 5, 6, 2], 1)


def test_2():
    test([1, 2, 3, 6, 5, 4, 0, 0], 3)


def test_3():
    test([1, 3, 3, 3, 2, 4, 2, 1, 2], 4)


if __name__ == "__main__":
    test_1()
    test_2()
    test_3()
