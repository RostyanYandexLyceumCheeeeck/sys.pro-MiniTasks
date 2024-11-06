# https://leetcode.com/problems/range-sum-query-mutable/submissions/1442932712
from copy import deepcopy


def num2up(x):
    y = 1
    while y < x:
        y <<= 1
    return y


class SegmentTree:
    def __init__(self, arr: list):
        k = num2up(len(arr))
        self.arr = [0] * (k - 1) + deepcopy(arr) + [0] * (k - len(arr))
        self.build_init()

    def build_init(self):
        for target in range(len(self.arr) // 2 - 1, -1, -1):
            l = 2 * target + 1
            r = l + 1

            self.arr[target] = 0
            if l < len(self.arr):
                self.arr[target] += self.arr[l]
            if r < len(self.arr):
                self.arr[target] += self.arr[r]

    def get_sum(self, left, right):
        return self.get_sum_rec(0, 0, len(self.arr) // 2, left, right)

    def get_sum_rec(self, target, v_left, v_right, left, right):
        if left == v_left and right == v_right:
            return self.arr[target]

        v_middle = (v_left + v_right) // 2
        res = 0

        if left <= v_middle:
            res += self.get_sum_rec(2 * target + 1, v_left, v_middle, left, min(right, v_middle))

        if right > v_middle:
            res += self.get_sum_rec(2 * target + 2, v_middle + 1, v_right, max(left, v_middle + 1), right)
        return res

    def update(self, pos, x):
        new_pos = len(self.arr) // 2 + pos
        self.update_rec(0, 0, len(self.arr) // 2, pos, x - self.arr[new_pos])

    def update_rec(self, target, v_left, v_right, pos, delta):
        self.arr[target] += delta
        if target == pos + len(self.arr) // 2:
            return

        v_middle = (v_left + v_right) // 2
        if pos <= v_middle:
            return self.update_rec(2 * target + 1, v_left, v_middle, pos, delta)
        return self.update_rec(2 * target + 2, v_middle + 1, v_right, pos, delta)


def test_1():
    mas = [46, 11, 40, 8, 2, 19, 65, 10]
    qwe = SegmentTree(mas)
    print(mas)
    print(qwe.arr)
    # print(qwe.get_sum(0, 0))
    # print(qwe.get_sum(0, 1))
    # print(qwe.get_sum(0, 2))

    for i in range(len(mas)):
        for j in range(i, len(mas)):
            # print(i, j)
            assert qwe.get_sum(i, j) == sum(mas[i:j + 1])


def test_2():
    mas = [5, 18, 13]
    qwe = SegmentTree(mas)
    print(mas)
    print(qwe.arr)

    assert qwe.get_sum(0, 2) == 36
    qwe.update(1, -1)  # [5, -1, 13]
    print(qwe.arr)
    qwe.update(2, 3)   # [5, -1, 3]
    print(qwe.arr)
    qwe.update(0, 5)   # [5, -1, 3]
    print(qwe.arr)
    qwe.update(0, -4)  # [-4, -1, 3]
    print(qwe.arr)
    assert qwe.get_sum(0, 2) == -2


if __name__ == "__main__":
    test_1()
    test_2()

