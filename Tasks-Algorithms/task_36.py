import time


class UnionFind:
    def __init__(self, size: int):
        self.rank: list[int] = [0] * size
        self.count: list[int] = [0] * size
        self.parent: list[int] = [i for i in range(size)]

    def find(self, elem: int):
        if self.parent[elem] != elem:
            self.parent[elem] = self.find(self.parent[elem])
        return self.parent[elem]

    def union(self, one_elem: int, two_elem: int):
        one_parent, two_parent = self.find(one_elem), self.find(two_elem)

        if self.rank[one_parent] < self.rank[two_parent]:
            self.parent[one_parent] = two_parent
            self.count[two_parent] += self.count[one_parent]
        else:
            self.parent[two_parent] = one_parent
            self.count[one_parent] += self.count[two_parent] * (one_parent != two_parent)
            self.rank[one_parent] += (self.rank[one_parent] == self.rank[two_parent])

    def get_free(self, elem):
        parent = self.find(elem)
        new_elem = (parent - self.count[parent]) % len(self.count)
        new_parent = self.find(new_elem)

        if self.count[new_parent] == 0:
            self.count[new_parent] += 1
            return new_parent

        self.union(parent, new_parent)
        return self.get_free(self.find(new_parent))


def scheduling(tasks: list[tuple[int, int]]):
    tasks.sort(key=lambda t: (-t[1], t[0]))
    size = len(tasks)
    search = UnionFind(size)
    schedule = [(0, 0)] * size

    for i in range(len(tasks) - 1):
        deadline, fine = tasks[i]

        parent = search.find(deadline)
        free = search.get_free(parent)

        schedule[free] = tasks[i]
        search.union(free, parent)

    for i in range(-1, -len(tasks) - 1, -1):
        if schedule[i] == (0, 0):
            schedule[i] = tasks[-1]
            break

    result_fine = 0
    for day in range(len(schedule)):
        deadline, fine = schedule[day]
        result_fine += fine * (deadline < day)

    print(schedule, sep=" -> ")
    return result_fine


def test0():
    arr = [(2, 25), (0, 30), (2, 50), (3, 10), (2, 15)]
    assert scheduling(arr) == 15


def test1():
    arr = [(0, 42), (1, 69), (2, 420), (3, 1997), (3, 23126), (4, 2005), (5, 0)]
    assert scheduling(arr) == 42


def test2():
    arr = []
    assert scheduling(arr) == 0


def test3():
    arr = [(11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1), (11, 1)]
    assert scheduling(arr) == 0


def test4():
    arr = [(11, 1), (1, 11), (1, 11), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1)]
    assert scheduling(arr) == 9


def test5():
    arr = [(0, 12), (1, 12), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (8, 11), (8, 12), (8, 12), (9, 12), (9, 1)]
    assert scheduling(arr) == 12


def test6():
    arr = [(0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12), (8, 11), (8, 12), (8, 13), (9, 12), (9, 1)]
    assert scheduling(arr) == 7


def check_time_test(func):
    print(f"=========== {func.__name__} ===========".center(32, "="))
    start = time.time()
    func()
    print(time.time() - start)
    print()


if __name__ == "__main__":
    check_time_test(test0)
    check_time_test(test1)
    check_time_test(test2)
    check_time_test(test3)
    check_time_test(test4)
    check_time_test(test5)
    check_time_test(test6)


