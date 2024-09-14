# https://leetcode.com/problems/redundant-connection/submissions/1389507097
fyr = 0


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
                self.count = min(self._father.count, fyr)
            return self._father

        @father.setter
        def father(self, value):
            new_count = min(len(value) + len(self), fyr)
            value.count = new_count
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

        self.vertices[one_v] = right.father
        left.father = right.father

    def find(self, vertex):
        return self.vertices[vertex].father.index


def check(arr):
    asd = UnionFind(len(arr))
    for i, j in arr:
        x, y = i - 1, j - 1
        if asd.find(x) == asd.find(y):
            return [i, j]

        asd.union(x, y)


def test_1():
    qwe = [[1, 2], [1, 3], [2, 3]]
    return check(qwe)  # [2, 3]


def test_2():
    qwe = [[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]]
    return check(qwe)  # [4, 1]


def test_3():
    zxc = [[3, 7], [1, 4], [2, 8], [1, 6], [7, 9], [6, 10], [1, 7], [2, 3], [8, 9], [5, 9]]
    qwe = [[3, 7], [1, 4], [2, 8], [1, 6], [7, 9], [6, 10], [1, 7], [2, 3], [8, 9], [5, 9]]
    return check(qwe)  # [8, 9]


def test_4():
    qwe = [[77, 89], [41, 89], [21, 92], [11, 17], [45, 90], [57, 81], [34, 89], [19, 45], [29, 74], [78, 82], [59, 72],
           [51, 63], [3, 90], [16, 46], [49, 91], [42, 79], [7, 66], [45, 67], [7, 72], [33, 65], [8, 64], [10, 56],
           [54, 92], [26, 43], [40, 88], [31, 75], [30, 75], [5, 23], [20, 61], [22, 45], [7, 22], [2, 27], [36, 56],
           [35, 91], [23, 80], [12, 73], [10, 68], [61, 83], [35, 68], [76, 100], [20, 37], [25, 100], [11, 84],
           [22, 40], [18, 34], [57, 60], [12, 28], [18, 42], [32, 71], [43, 53], [92, 98], [1, 43], [5, 81], [10, 52],
           [11, 48], [84, 85], [29, 59], [95, 100], [9, 44], [65, 96], [12, 25], [33, 38], [93, 97], [8, 49], [50, 100],
           [6, 38], [1, 24], [23, 79], [9, 99], [27, 98], [2, 8], [33, 99], [1, 55], [17, 51], [9, 62], [56, 71],
           [47, 48], [1, 50], [23, 94], [44, 79], [32, 97], [39, 95], [38, 86], [21, 25], [61, 70], [58, 97], [75, 85],
           [13, 78], [63, 78], [13, 69], [3, 26], [4, 47], [28, 31], [79, 87], [1, 14], [46, 97], [82, 98], [18, 88],
           [15, 56], [37, 54]]

    return check(qwe)  # [82, 98]


def test_5():
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
    # print(test_5())
