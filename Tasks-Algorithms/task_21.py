from math import inf
from copy import copy
from random import randint


class BinomialTree:
    def __init__(self, value=None, father=None, baby_right=None, baby_left=None, neighbour=None, degree: int = 0):
        self.value = value
        self.degree = degree
        self.father = father
        self.baby_left = baby_left
        self.baby_right = baby_right
        self.neighbour_left = neighbour

    def bind_baby(self, other):
        if self.degree < 2:
            return

        old = self.baby_left.baby_left
        new = other.baby_right
        while old:
            old.neighbour_left = new
            old = old.baby_left
            new = new.neighbour_left
            new = new.baby_right

    def merge(self, other):
        if self.degree != other.degree:
            raise ValueError
        if other.value < self.value:
            return other.merge(self)

        if self.degree:
            self.baby_left.neighbour_left = other
            self.bind_baby(other)

        self.baby_left = other
        other.father = self
        self.degree += 1

        if not other.degree:  # if self.degree == 1
            self.baby_right = other
        return self

    def sort_to_up(self):
        if self.father and self.father.value > self.value:
            self.value, self.father.value = self.father.value, self.value
            self.father.sort_to_up()

    def sort_to_down(self):
        if self.baby_left and self.baby_left.value < self.value:
            self.value, self.baby_left.value = self.baby_left.value, self.value
            self.baby_left.sort_to_down()


class BinomialHeap:
    def __init__(self, roots=None):
        self.roots = roots
        self.before_min = None
        self.min = None

    def insert(self, value):
        other = BinomialTree(value)
        self.roots = self.merge(BinomialHeap(other)).roots

    def peek_min(self):
        if self.min:
            return self.min.value

        head = self.roots
        self.min = head
        self.before_min = temp = None
        while head:
            if head.value < self.min.value:
                self.min = head
                self.before_min = temp
            head = head.neighbour_left
            temp = head
        return self.min.value

    def extract_min(self):
        res = self.peek_min()

        # delete minimum
        if self.before_min:
            self.before_min.neighbour_left = self.min.neighbour_left
        else:
            self.roots = self.min.neighbour_left

        self.roots = self.merge(BinomialHeap(self.min.baby_right)).roots
        self.before_min = self.min = None
        return res

    def decrease_key(self, link: BinomialTree, key):
        link.value = key
        link.sort_to_up()
        link.sort_to_down()

    def merge(self, other):
        if not other or not other.roots:
            return self

        if not self or not self.roots:
            return other

        result = BinomialHeap()
        result.roots = BinomialTree()
        result.min = self.min
        if other.min and self.min and other.min < self.min:
            result.min = other.min

        head_res = result.roots
        head_self = self.roots
        head_other = other.roots
        carry: BinomialTree | None = None

        while head_self or head_other:
            head_res.father = None

            if not head_self:
                if not carry:
                    head_res.neighbour_left = head_other
                    break
                elif carry.degree < head_other.degree:
                    carry.neighbour_left = head_other
                    head_res.neighbour_left = carry
                    carry = None
                    break

                carry = carry.merge(head_other)
                head_other = head_other.neighbour_left
                carry.neighbour_left = None
                continue

            elif not head_other:
                if not carry:
                    head_res.neighbour_left = head_self
                    break

                elif carry.degree < head_self.degree:
                    carry.neighbour_left = head_self
                    head_res.neighbour_left = carry
                    carry = None
                    break

                carry = carry.merge(head_self)
                head_self = head_self.neighbour_left
                carry.neighbour_left = None
                continue

            elif not carry:
                if head_self.degree < head_other.degree:
                    head_res.neighbour_left = head_self
                    head_self = head_self.neighbour_left
                    head_res = head_res.neighbour_left

                elif head_self.degree == head_other.degree:
                    carry = head_self.merge(head_other)
                    head_self = head_self.neighbour_left
                    head_other = head_other.neighbour_left
                    carry.neighbour_left = None

                else:
                    head_res.neighbour_left = head_other
                    head_other = head_other.neighbour_left
                    head_res = head_res.neighbour_left
                continue

            if head_self.degree == head_other.degree == carry.degree:
                head_res.neighbour_left = head_self  # add head_self
                head_res = head_self
                head_self = head_self.neighbour_left
                # head_res.neighbour_left = None

                carry = carry.merge(head_other)
                head_other = head_other.neighbour_left
                carry.neighbour_left = None

            elif head_self.degree > carry.degree < head_other.degree:
                head_res.neighbour_left = carry
                head_res = carry
                carry = None

            elif head_self.degree == carry.degree:
                carry = carry.merge(head_self)
                head_self = head_self.neighbour_left
                carry.neighbour_left = None

            else:  # head_self.degree > head_other.degree == carry.degree
                carry = carry.merge(head_other)
                head_other = head_other.neighbour_left
                carry.neighbour_left = None

        if carry:
            carry.father = None
            head_res.neighbour_left = carry

        result.roots = result.roots.neighbour_left
        return result

    def delete(self, link):
        self.decrease_key(link, -inf)
        self.extract_min()

    def heap_to_number(self):
        res = 0
        head = self.roots
        while head:
            res += 2 ** head.degree
            head = head.neighbour_left

        return res


def createBinomialTree(size, arr: list | None = None, shift: int = 0) -> BinomialTree:
    if not size:
        return BinomialTree()

    if not arr:
        arr = [shift + x for x in range(size)]

    size = len(arr)

    arr = copy(arr)
    for i in range(len(arr)):
        arr[i] = BinomialTree(arr[i])

    step = 1
    while step < size:
        for i in range(0, size - step, 2 * step):
            arr[i] = arr[i].merge(arr[i + step])
        step *= 2
    return arr[i]


def createBinomialHeap(pattern: int | str = '0', shift: int = 0) -> BinomialHeap:
    if isinstance(pattern, int):
        pattern = bin(pattern)[2:]

    res = BinomialHeap()
    size = 1
    for i in range(-1, -len(pattern) - 1, -1):
        bit = int(pattern[i])
        if bit:
            temp = createBinomialTree(size, shift=size - 1 + shift)
            res = res.merge(BinomialHeap(temp))
        size *= 2
    return res


def testing_insert(heap: BinomialHeap, value):
    before = heap.heap_to_number()
    heap.insert(value)
    after = heap.heap_to_number()
    assert after == before + 1


def testing_extract_min(heap: BinomialHeap):
    before = heap.heap_to_number()
    res = heap.extract_min()
    print('ext_min = ', res)
    after = heap.heap_to_number()
    assert after == before - 1


def testing_decrease_key(heap: BinomialHeap, elem, key):
    heap.decrease_key(elem, key)
    t = 3   # не знаю, как ассёртом проверить. Тестил дебаггером в пайчарме >_<


def testing_delete(heap: BinomialHeap, elem):
    before = heap.heap_to_number()
    heap.delete(elem)
    after = heap.heap_to_number()
    assert after == before - 1


if __name__ == "__main__":
    one = createBinomialTree(8)

    qwe = createBinomialHeap('1101')

    asd = createBinomialHeap('1111', 15)

    zxc = asd.merge(qwe)  # '11100'

    testing_insert(zxc, 0)
    testing_extract_min(zxc)
    testing_decrease_key(zxc, zxc.roots.neighbour_left.baby_left, -1)
    testing_delete(zxc, zxc.roots)
