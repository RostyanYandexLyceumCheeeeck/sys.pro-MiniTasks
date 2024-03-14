# https://leetcode.com/problems/merge-k-sorted-lists/submissions/1203796613
from copy import copy
from random import randint, shuffle


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class PriorityQueue:
    def __init__(self, arr=None, key_sort=lambda x: x, non_growing: bool = True, func_filter=lambda x: x):
        if arr is None:
            arr = list()

        self.key = key_sort
        self.func = lambda x, y: self.key(x) < self.key(y) if non_growing else self.key(x) > self.key(y)
        self.queue = [x for x in arr if func_filter(x)]
        if len(self.queue):
            self.heap_sort()

    def add_to_sheet(self, value):
        self.queue.append(value)
        self.sort_from_sheet()

    def add_to_top(self, value):
        self.queue.append(value)
        self.swap_first_and_last()

    def pop_top(self):
        res = self.queue[0]
        self.queue[0], self.queue[-1] = self.queue[-1], self.queue[0]
        self.queue.pop()
        self.sort_from_top()
        return res

    def peek_top(self):
        return self.queue[0]

    def change_priority_top(self, func: lambda x: x):
        self.queue[0] = func(self.queue[0])
        self.sort_from_top()

    def sort_from_sheet(self, end: int | None = None):
        if end is None:
            end = len(self.queue) - 1

        i = end
        j = i // 2
        while i and self.func(self.queue[j], self.queue[i]):
            self.queue[j], self.queue[i] = self.queue[i], self.queue[j]
            i = j
            j //= 2

    def sort_from_top(self, start: int = 0, end: int | None = None):
        if end is None:
            end = len(self.queue)

        i = start
        while i < end:
            t = i
            l = 2 * i + 1
            r = 2 * i + 2

            if l < end and self.func(self.queue[t], self.queue[l]):
                t = l
            if r < end and self.func(self.queue[t], self.queue[r]):
                t = r

            if t != i:
                self.queue[t], self.queue[i] = self.queue[i], self.queue[t]
                i = t
            else:
                break

    def swap_first_and_last(self, start: int = 0, end: int = -1):
        self.queue[start], self.queue[end] = self.queue[end], self.queue[start]
        self.sort_from_top(start)
        self.sort_from_sheet(end)

    def heap_sort(self):
        if len(self.queue) < 2:
            return

        start = len(self.queue) // 2 - (len(self.queue) + 1) % 2
        for i in range(start, -1, -1):
            self.sort_from_top(i)

    def __len__(self):
        return len(self.queue)


def merge_k_lists(arr):
    queue = PriorityQueue(arr, key_sort=lambda x: x.val, non_growing=False, func_filter=lambda x: not (x is None))
    head = c_head = ListNode()
    while len(queue):
        temp = queue.peek_top()
        c_head.next = ListNode(temp.val)
        c_head = c_head.next
        if temp.next is None:
            queue.pop_top()
        else:
            queue.change_priority_top(func=lambda x: x.next)

    return head.next


def createListNode(left: int = 0, right: int = 10):
    if not left:
        left += 1
    mas = [i for i in range(left, right)]
    head = one = ListNode()
    for x in mas:
        one.next = ListNode(x)
        one = one.next

    return head.next


def myPrintListNode(head):
    new_head = copy(head)
    while new_head:
        print(new_head.val, end=' ')
        new_head = new_head.next
    print()


if __name__ == "__main__":
    zxc = [createListNode() for x in range(10)]
    myPrintListNode(merge_k_lists(zxc))
