# https://leetcode.com/problems/count-of-smaller-numbers-after-self/submissions/1445329046

import math
from copy import deepcopy


def num2up(x):
    y = 1
    while y < x:
        y <<= 1
    return y


class Value:
    def __init__(self, value, count_left=0, count_right=0):
        self.value = value
        self.count_left = count_left
        self.count_right = count_right

    def __eq__(self, other):
        return self.value == other.value

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value


class Root:
    def __init__(self, mas, left=None, right=None):
        self.arr: list[Value] = mas
        # self.value = value
        self.left = left
        self.right = right

    @staticmethod
    def merge(left, right):
        mas: list[Value] = []
        i, j = 0, 0
        while i < len(left.arr) and j < len(right.arr):
            if left.arr[i] < right.arr[j]:
                mas.append(Value(left.arr[i].value, i, j))
                i += 1
            else:
                mas.append(Value(right.arr[j].value, i, j))
                j += 1

            if len(mas) > 1 and mas[-1].value == mas[-2].value:
                mas[-1].count_left = mas[-2].count_left
                mas[-1].count_right = mas[-2].count_right

        while i < len(left.arr):
            mas.append(Value(left.arr[i].value, i, j))
            i += 1
            if len(mas) > 1 and mas[-1].value == mas[-2].value:
                mas[-1].count_left = mas[-2].count_left
                mas[-1].count_right = mas[-2].count_right

        while j < len(right.arr):
            mas.append(Value(right.arr[j].value, i, j))
            j += 1
            if len(mas) > 1 and mas[-1].value == mas[-2].value:
                mas[-1].count_left = mas[-2].count_left
                mas[-1].count_right = mas[-2].count_right

        return Root(mas, left, right)

    def bisect(self, x):
        vx = Value(x)
        if self.arr[0] >= vx:
            return 0

        left, right = 0, len(self.arr) - 1
        target = (left + right) // 2
        while left < target < right:
            if self.arr[target] < vx:
                left = target
            else:
                right = target
            target = (left + right) // 2

        return left if self.arr[left] >= vx else (target if self.arr[target] >= vx else right)
        # return right if self.arr[right] == vx else (target if self.arr[target] == vx else left)


class SegmentTree:
    def __init__(self, arr: list):
        k = num2up(len(arr))
        self.root = self.merge_sort(arr + [math.inf] * (k - len(arr)))
        # self.build_init()

    def build_init(self, arr):
        pass

    def merge_sort(self, arr):
        if not arr:
            return
        if len(arr) == 1:
            return Root([Value(arr[0])])

        left = self.merge_sort(arr[:len(arr)//2])
        right = self.merge_sort(arr[len(arr)//2:])
        return Root.merge(left, right)

    def get_k(self, left, right, target):
        ind_up = self.root.bisect(target)
        return self.get_k_rec(self.root, 0, len(self.root.arr) - 1, left, right, ind_up)

    def get_k_rec(self, target_root: Root, v_left, v_right, left, right, ind_up):
        if left == v_left and right == v_right:
            return ind_up
        if target_root and ind_up == len(target_root.arr):
            return right - left
        if not ind_up:
            return 0
        # ind_up = min(ind_up, len(target_root.arr) - 1)

        v_middle = (v_left + v_right) // 2
        res = 0

        if left <= v_middle:
            res += self.get_k_rec(target_root.left, v_left, v_middle, left, min(right, v_middle),
                                  target_root.arr[ind_up].count_left)
        if right > v_middle:
            res += self.get_k_rec(target_root.right, v_middle + 1, v_right, max(left, v_middle + 1), right,
                                  target_root.arr[ind_up].count_right)
        return res


def test_1():
    arr = [5, 2, 6, 1]
    tree = SegmentTree(arr)
    res = [tree.get_k(i + 1, len(arr) - 1, arr[i]) for i in range(len(arr))]

    print(res)
    assert res == [2, 1, 1, 0]

"""
1 2 5 6
2 5 || 1 6
5 | 2 || 6 | 1

"""


if __name__ == "__main__":
    test_1()
