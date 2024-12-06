from bisect import bisect_right, bisect_left
from copy import copy


class Node:
    def __init__(self, start, end, rec_build=True):
        self.end = end
        self.count = 0
        self.start = start

        self.left: Node | None = None
        self.right: Node | None = None
        if rec_build:
            self.build_init()

    def build_init(self):
        l, r = self.start, self.end
        if l == r:
            return

        m = (l + r) >> 1
        self.left = Node(l, m)
        self.right = Node(m + 1, r)
        self.count = self.left.count + self.right.count

    def reincarnation(self, ind):
        node = copy(self)
        node.count += 1
        if node.start == node.end:
            return node

        m = (node.start + node.end) >> 1
        if ind <= m:
            node.left = node.left.reincarnation(ind)
        else:
            node.right = node.right.reincarnation(ind)
        return node

    def __copy__(self):
        res = Node(self.start, self.end, False)
        res.left = self.left
        res.right = self.right
        res.count = self.count
        return res


class PersistentSegmentTree:
    def __init__(self, arr):
        self.versions: list[Node | None] = [None] * (len(arr) + 1)
        self.versions[0] = Node(0, len(arr) - 1)
        self.arr = sorted(arr)
        self.last_version = 0
        self.build_init(arr)

    def build_init(self, arr):
        table = {}
        for i in range(len(arr)):
            elem = arr[i]
            if elem in table:
                table[elem].append(i)
            else:
                table[elem] = [i]

        for elem in self.arr[::-1]:
            for ind in table[elem]:
                self.reincarnation(ind)
            table[elem] = []

    def reincarnation(self, ind):
        self.last_version += 1
        self.versions[self.last_version] = self.versions[self.last_version - 1].reincarnation(ind)

    def gte(self, l, r, target):
        ind = bisect_left(self.arr, target)
        return self.gte_rec(self.versions[len(self.arr) - ind], l, r)

    def gte_rec(self, node: Node, l, r):
        if l == node.start and r == node.end:
            return node.count

        res = 0
        m = (node.start + node.end) >> 1
        if l <= m:
            res += self.gte_rec(node.left, l, min(r, m))
        if r > m:
            res += self.gte_rec(node.right, max(l, m + 1), r)
        return res


def my_assert(pst, arr, l, r, target):
    print(pst.gte(l, r, target))
    assert pst.gte(l, r, target) == len([x for x in arr[l:r+1] if x >= target])


def test_1():
    arr = [6, 2, 7, 8, 1, 0, 4]
    pst = PersistentSegmentTree(arr)

    my_assert(pst, arr, 2, 5, 2)
    my_assert(pst, arr, 0, 6, -1)
    my_assert(pst, arr, 0, 0, 1)
    my_assert(pst, arr, 0, 0, 6)
    my_assert(pst, arr, 0, 0, 9)


def test_2():
    arr = [-1, -1]
    pst = PersistentSegmentTree(arr)

    my_assert(pst, arr, 1, 1, -1)


if __name__ == "__main__":
    test_1()
    test_2()
