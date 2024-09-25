class UnionFind:
    def __init__(self, size: int):
        self.parent: list[int] = [i for i in range(size)]

    def find(self, elem: int):
        if self.parent[elem] != elem:
            self.parent[elem] = self.find(self.parent[elem])
        return self.parent[elem]

    def union(self, one_elem: int, two_elem: int):
        one_parent, two_parent = self.find(one_elem), self.find(two_elem)
        self.parent[two_parent] = one_parent


def scheduling(tasks: list[tuple[int, int]]):
    tasks.sort(key=lambda t: (-t[1], t[0]))
    size = len(tasks)
    search = UnionFind(size)
    schedule = [(0, 0)] * size

    for i in range(len(tasks)):
        deadline, fine = tasks[i]

        parent = search.find(deadline)
        schedule[parent] = tasks[i]

        x = max(parent - 1, -(parent - 1) * size - 1)  # parent or (size - 1)
        search.union(x, parent)

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


if __name__ == "__main__":
    test0()
    test1()
    test2()
    test3()
    test4()


