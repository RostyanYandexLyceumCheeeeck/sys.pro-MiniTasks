# https://leetcode.com/problems/reverse-linked-list-ii/submissions/1194505570
from copy import copy


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


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


def reverseBetween(head, left: int, right: int):
    if left >= right:
        return head

    new_head = new_list = head if left > 1 else ListNode(0, head)
    count = 1
    while count < left:
        count += 1
        head = head.next
        if count == left:
            break
        new_list = new_list.next

    # myPrintListNode(new_list)
    # myPrintListNode(head)
    # new_list.next = None
    # myPrintListNode(new_head)

    start = new_list
    ptr = head
    head = head.next
    count += 1
    while count <= right:
        temp = copy(head)
        ptr.next = temp.next
        temp.next = start.next
        start.next = temp
        head = head.next
        count += 1

    return new_head if left > 1 else new_head.next


def empty(head):
    return


def title_factory(objs, length):
    res = []
    for name, sep, value, end in objs:
        res.append(f"{name}{sep}{value}{end}")
    res = "".join(res).center(length, '=')
    return res


def test_factory(left: int, right: int, el_min: int = 0, el_max: int = 10, debug: bool = False, number_test: int = -1):
    title = {'values': [title_factory([("TEST", ' ', number_test, '')], 30),
                        title_factory([('left', '=', left, ' '), ('right', '=', right, '')], 30)],
             'end': '\n'} if number_test > -1 else {'values': '', 'end': ''}
    func = myPrintListNode if debug else empty

    arr = createListNode(el_min, el_max)
    print(*title['values'], sep='\n', end=title['end'])
    func(arr)
    arr = reverseBetween(arr, left, right)
    func(arr)
    func(None)


def base_test():
    test_factory(2, 4, 1, 6, True, 1)
    test_factory(3, 4, 1, 6, True, 2)
    test_factory(3, 5, 1, 6, True, 3)
    test_factory(1, 4, 1, 6, True, 4)
    test_factory(1, 5, 1, 6, True, 5)


if __name__ == "__main__":
    base_test()
