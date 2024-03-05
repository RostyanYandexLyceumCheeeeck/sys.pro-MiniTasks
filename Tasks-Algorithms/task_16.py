# https://leetcode.com/problems/linked-list-cycle-ii/submissions/1193382167

import copy
from random import randint


def factory(x: int, y: int = 0):
    res = LinkedList([t for t in range(x)])
    res.create_cycle(y)
    return res


def base_test():
    one = LinkedList([3, 2, 0, -4])
    one.create_cycle(1)

    two = LinkedList([1, 2])
    two.create_cycle()

    three = LinkedList([1])

    assert search_cycle(one.head) == 1
    assert search_cycle(two.head) == 0
    assert search_cycle(three.head) == -1


def test1(count: int = 100):
    for i in range(count):
        x = randint(100, 1000)
        y = randint(1, x)
        first = factory(x, y)
        t = search_cycle(first.head)
        flag = t == y
        if not flag:
            print(x, y, t)
        assert flag


class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node


class LinkedList:
    def __init__(self, arr: list | None = None):
        self.head = self.pos = self.tail = None
        if isinstance(arr, list):
            for el in arr:
                self.add_to_tail(el)

    def add_to_head(self, val):
        node = Node(val, self.head)
        self.head = node
        if not self.tail:
            self.tail = self.head

    def add_to_tail(self, val):
        node = Node(val)
        if self.tail:
            self.tail.next_node = node
            self.tail = node
        else:
            self.head = self.tail = node

    def __iter__(self):
        self.pos = self.head
        return self

    def __next__(self):
        if self.pos:
            res = self.pos
            self.pos = self.pos.next_node
            return res.value
        raise StopIteration

    def create_cycle(self, ind_start: int = 0):
        if self.head is None:
            return
        self.pos = self.head

        for _ in range(ind_start):
            if not (self.pos.next_node is None):
                self.pos = self.pos.next_node
            else:
                self.pos.next_node = self.head
                self.pos = self.head
                return

        self.tail.next_node = self.pos
        self.pos = self.head


def search_cycle(head):
    start = new_start = head

    for _ in range(2):
        if new_start.next_node is None:
            return -1
        new_start = new_start.next_node
    start = start.next_node

    while start != new_start:
        for _ in range(2):
            if new_start.next_node is None:
                return -1
            new_start = new_start.next_node
        start = start.next_node

    start = head
    result = 0

    while start != new_start:
        start = start.next_node
        new_start = new_start.next_node
        result += 1

    return result


if __name__ == "__main__":
    base_test()
    test1(1000)
