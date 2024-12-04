import math
import time

DEBUG = True


def decorator(func):
    def wrapper(*args, **kwargs):
        start = 0
        if DEBUG:
            print(f"=========== {func.__name__} ===========".center(32, "="))
            start = time.time()
        func(*args, **kwargs)
        if DEBUG:
            print(time.time() - start)
            print()
    return wrapper


class UnionFind:
    def __init__(self, size: int):
        self.rank: list[int] = [0] * size
        self.parent: list[int] = [i for i in range(size)]
        self.vacancy: list[int] = [(i - 1) % size for i in range(size)]

    def find(self, elem: int):
        if self.parent[elem] != elem:
            self.parent[elem] = self.find(self.parent[elem])
        return self.parent[elem]

    def union(self, one_elem: int, two_elem: int):
        if one_elem == two_elem and not self.rank[one_elem]:
            self.rank[one_elem] += 1
            return

        one_parent, two_parent = self.find(one_elem), self.find(two_elem)

        if one_parent == two_parent:
            return

        if two_parent < one_parent:
            return self.union(two_elem, one_elem)

        if self.rank[one_parent] < self.rank[two_parent]:
            self.vacancy[two_parent] = self.vacancy[one_parent if self.find(self.vacancy[two_parent]) == one_parent
                                                    else two_parent]
            self.parent[one_parent] = two_parent

        else:
            self.vacancy[one_parent] = self.vacancy[two_parent if self.find(self.vacancy[one_parent]) == two_parent
                                                    else one_parent]
            self.parent[two_parent] = one_parent
            self.rank[one_parent] += (self.rank[one_parent] == self.rank[two_parent])

    def get_free(self, elem):
        parent = self.find(elem)
        if not self.rank[parent]:
            return parent

        new_elem = self.vacancy[parent]
        new_parent = self.find(new_elem)
        if new_elem == new_parent and not self.rank[new_parent]:
            return new_parent

        self.union(new_parent, parent)
        return self.get_free(new_parent)


def scheduling(tasks: list[tuple[int, int]]):
    tasks.sort(key=lambda t: (-t[1], t[0]))
    size = len(tasks)
    search = UnionFind(size)
    schedule = [(0, 0)] * size

    for i in range(len(tasks)):
        deadline, fine = tasks[i]

        parent = search.find(deadline)
        free = search.get_free(parent)

        schedule[free] = tasks[i]
        search.union(free, parent)

    result_fine = 0
    for day in range(len(schedule)):
        deadline, fine = schedule[day]
        result_fine += fine * (deadline < day)

    print(schedule, sep=" -> ")
    return result_fine


@decorator
def test00():
    arr = [(2, 25), (0, 30), (2, 50), (3, 10), (2, 15)]
    assert scheduling(arr) == 15


@decorator
def test01():
    arr = [(0, 42), (1, 69), (2, 420), (3, 1997), (3, 23126), (4, 2005), (5, 0)]
    assert scheduling(arr) == 42


@decorator
def test02():
    arr = []
    assert scheduling(arr) == 0


@decorator
def test03():
    arr = [(11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1)]
    assert scheduling(arr) == 0


@decorator
def test04():
    arr = [(11, 1), (1, 11), (1, 11), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1)]
    assert scheduling(arr) == 9


@decorator
def test05():
    arr = [(0, 12), (1, 12), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (8, 11), (8, 12), (8, 12), (9, 12), (9, 1)]
    assert scheduling(arr) == 12


@decorator
def test06():
    arr = [(0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12), (8, 11), (8, 12), (8, 13), (9, 12), (9, 1)]
    assert scheduling(arr) == 7


@decorator
def test07():
    arr = [(0, 12), (1, 12), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (6, 11), (6, 10), (6, 9), (6, 8), (11, 1)]
    assert scheduling(arr) == 38


@decorator
def test08():
    arr = [(0, 8), (0, 38)]
    assert scheduling(arr) == 8


@decorator
def test09():
    arr = [(0, 8), (0, 0)]
    assert scheduling(arr) == 0


@decorator
def test10():
    arr = [(0, 8), (0, 1), (0, 1), (0, 1), (0, 7)]
    assert scheduling(arr) == 10


@decorator
def test11():
    arr = [(3, 30), (2, 20), (1, 10), (0, 15), (2, 25)]
    assert scheduling(arr) == 10


def all_tests():
    test00()
    test01()
    test02()
    test03()
    test04()
    test05()
    test06()
    test07()
    test08()
    test09()
    test10()
    test11()


if __name__ == "__main__":
    all_tests()
    