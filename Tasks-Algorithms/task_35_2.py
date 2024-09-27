# https://leetcode.com/problems/redundant-connection-ii/submissions/1404333732
class UnionFind:
    class Node:
        def __init__(self, index, father=None):
            self._father = father if father else self
            self.index = index
            self.count = 1

        @property
        def father(self):
            if self._father != self:
                self._father = self._father.father
                self.index = self._father.index
            return self._father

        @father.setter
        def father(self, value):
            self._father._father = value
            self.index = value.index

        def __len__(self):
            return self.father.count

    def __init__(self, vertices):
        self.vertices = [UnionFind.Node(v) for v in range(vertices)]

    def union(self, one_v, two_v):
        left, right = self.vertices[one_v], self.vertices[two_v]

        if len(right) < len(left):
            return self.union(two_v, one_v)

        if left.father == right.father:
            return

        right.father.count += len(left)
        self.vertices[one_v] = right.father
        left.father = right.father

    def find(self, vertex):
        return self.vertices[vertex].father.index


def proobr(arr):
    return [arr[0] + 1, arr[1] + 1]


def check(arr):
    asd = UnionFind(len(arr))
    count = {i: [] for i in range(len(arr))}
    target = None
    cycle = None

    for i, j in arr:
        x, y = i - 1, j - 1
        count[y].append([x, y])

        if len(count[y]) > 1:
            target = y
        elif asd.find(x) == asd.find(y):
            cycle = [x, y]
        else:
            asd.union(x, y)

    # print(target, cycle)
    # print(count.values())
    if target is None:
        return proobr(cycle)

    x = asd.find(0)
    for i in range(len(arr)):
        # print(asd.find(i))
        if x != asd.find(i):
            return proobr(count[target][0])
    return proobr(count[target][1])


def test_1():
    qwe = [[1, 2], [1, 3], [2, 3]]
    return check(qwe)  # [2, 3]


def test_2():
    qwe = [[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]]
    return check(qwe)  # [4, 1]


def test_3():
    qwe = [[2, 1], [3, 1], [4, 2], [1, 4]]
    return check(qwe)  # [2, 1]


def test_4():
    qwe = [[3, 1], [2, 1], [4, 2], [1, 4]]
    return check(qwe)  # [2, 1]


def test_5():
    qwe = [[3, 5], [1, 3], [2, 1], [5, 4], [2, 3]]
    return check(qwe)  # [2, 3]


def test_11():
    a = 1 << 4
    asd = UnionFind(a)

    j = 1
    while j < a:
        for i in range(0, a - j, 2 * j):
            asd.union(i, i + j)
            print(i, i + j, asd.find(i), asd.find(i + j))
        print()
        j <<= 1

    for i in range(a):
        print(f"{i} -- {asd.find(i)}")


if __name__ == "__main__":
    print(test_1())
    print(test_2())
    print(test_3())
    print(test_4())
    print(test_5())
