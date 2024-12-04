# https://leetcode.com/problems/count-of-smaller-numbers-after-self/submissions/1466527793
from bisect import bisect_left


class Node:
    def __init__(self, start, end, arr):
        self.arr = arr
        self.end = end
        self.left = None
        self.right = None
        self.start = start

        self.index_left = None
        self.index_right = None
        self.build_init(start, end, arr)

    def build_init(self, l, r, arr):
        self.arr = arr[l:r+1]
        if l == r:
            return

        m = (self.start + self.end) >> 1
        self.left = Node(l, m, arr)
        self.right = Node(m + 1, r, arr)
        self.index_left = [0] * (r - l + 1)
        self.index_right = [0] * (r - l + 1)
        self.merge_child()

    def merge_child(self):
        i, j = 0, 0
        first = self.left.arr if self.left else []
        second = self.right.arr if self.right else []

        while i < len(first) and j < len(second):
            flag = first[i] < second[j]
            k = i + j
            self.arr[k] = first[i] if flag else second[j]
            self.index_left[k] = i
            self.index_right[k] = j
            i += flag
            j += not flag

        while i < len(first):
            k = i + j
            self.arr[k] = first[i]
            self.index_left[k] = i
            self.index_right[k] = j
            i += 1

        while j < len(second):
            k = i + j
            self.arr[k] = second[j]
            self.index_left[k] = i
            self.index_right[k] = j
            j += 1

        for t in range(1, i + j):
            if self.arr[t] == self.arr[t - 1]:
                self.index_left[t] = self.index_left[t - 1]
                self.index_right[t] = self.index_right[t - 1]


class SegmentTree:
    def __init__(self, arr):
        self.root = Node(0, len(arr) - 1, arr)

    def gte(self, l, r, target):
        ind = bisect_left(self.root.arr, target)
        return self.gte_rec(self.root, l, r, ind)

    def gte_rec(self, node: Node, l, r, ind):
        if l == node.start and r == node.end:
            return ind
        if ind >= len(node.arr):
            return 0

        res = 0
        m = (node.start + node.end) >> 1
        if l <= m:
            res += self.gte_rec(node.left, l, min(r, m), node.index_left[ind])
        if r > m:
            res += self.gte_rec(node.right, max(l, m + 1), r, node.index_right[ind])
        return res


def test_1():
    arr = [5, 2, 6, 1]
    tree = SegmentTree(arr)
    res = [tree.gte(i + 1, len(arr) - 1, arr[i]) for i in range(len(arr))]

    # print(res)
    assert res == [2, 1, 1, 0]


"""
1 2 5 6
2 5 || 1 6
5 | 2 || 6 | 1

"""

if __name__ == "__main__":
    test_1()
