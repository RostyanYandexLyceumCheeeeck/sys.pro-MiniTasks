from math import inf


class BinomialTree:
    def __init__(self, value=None, father=None, baby=None, neighbour=None, degree: int = 0):
        self.value = value
        self.degree = degree
        self.father = father
        self.baby_left = baby
        self.baby_right = baby
        self.neighbour_left = neighbour

    def bind_baby(self, other):
        if self.degree < 1:
            return

        old = self.baby_left.baby_left
        new = other.baby_right
        while old:
            old.neighbour_left = new
            old = old.baby_left
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

        if not other.degree:
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
        self.min = None

    def insert(self, value):
        other = BinomialTree(value)
        self.merge(BinomialHeap(other))

    def peek_min(self):
        if self.min:
            return self.min.value

        head = self.roots
        self.min = head
        while head:
            if head.value < self.min.value:
                self.min = head
            head = head.neighbour_left
        return self.min.value

    def extract_min(self):
        res = self.peek_min()
        self.merge(res.baby_right)
        return res

    def decrease_key(self, link: BinomialTree, key):
        link.value = key
        link.sort_to_up()
        link.sort_to_down()

    def merge(self, other):
        other.roots.father = None
        previous_head_res = self.roots
        previous_head_other = other.roots
        head_res = self.roots
        head_other = other.roots
        carry = None

        while head_res or head_other or carry:
            if head_other:
                head_other.father = None

            if head_res is None:
                if carry is None:  # only head_other
                    previous_head_other.neighbour_left = None
                    previous_head_res.neighbour_left = head_other
                    break
                if head_other is None:  # only carry
                    previous_head_res.neighbour_left = carry
                    break
                if carry.degree < head_other.degree:
                    carry.neighbour_left = head_other
                    previous_head_res.neighbour_left = carry
                    break
                carry = carry.merge(head_other)
                carry.neighbour_left = None
                previous_head_other = head_other
                head_other = head_other.neighbour_left
                continue

            if head_other is None:
                if carry is None:  # only head_res
                    break
                if carry.degree < head_res.degree:
                    carry.neighbour_left = head_res
                    previous_head_res.neighbour_left = carry
                    break
                carry = carry.merge(head_res)
                carry.neighbour_left = None
                previous_head_res = head_res
                head_res = head_res.neighbour_left
                continue

            if carry is None:
                if head_res.degree < head_other.degree:
                    previous_head_res = head_res
                    head_res = head_res.neighbour_left
                    continue

                if head_res.degree == head_other.degree:
                    carry = head_res.merge(head_other)
                    carry.neighbour_left = None
                    previous_head_res.neighbour_left = head_res.neighbour_left
                    head_res = head_res.neighbour_left

                elif head_res.degree > head_other.degree:
                    previous_head_res.neighbour_left = head_other
                    previous_head_res = head_other

                previous_head_other = head_other
                head_other = head_other.neighbour_left
                continue

            # head_res and head_other and carry
            if head_res.degree > carry.degree < head_other.degree:
                carry.neighbour_left = head_other if head_other.degree < head_res.degree else head_res
                previous_head_res.neighbour_left = carry
                previous_head_res = carry
                carry = None

            elif head_res.degree == carry.degree == head_other.degree:
                carry = carry.merge(head_other)
                carry.neighbour_left = None
                previous_head_res = head_res
                previous_head_other = head_other
                head_res = head_res.neighbour_left
                head_other = head_other.neighbour_left
                # continue

            elif head_res.degree == carry.degree:
                carry = carry.merge(head_res)
                carry.neighbour_left = None
                previous_head_res.neighbour_left = head_res.neighbour_left
                previous_head_res = head_res
                head_res = head_res.neighbour_left

            else:  # head_res.degree > carry.degree == head_other_degree
                carry = carry.merge(head_other)
                carry.neighbour_left = head_res
                previous_head_res.neighbour_left = carry
                previous_head_res = carry
                previous_head_other = head_other
                head_other = head_other.neighbour_left

        return self.roots

    def delete(self, link):
        self.decrease_key(link, -inf)
        self.extract_min()


if __name__ == "__main__":
    one = BinomialTree(1)
    two = BinomialTree(2)
    three = BinomialTree(3)
    four = BinomialTree(4)
    five = BinomialTree(5)
    six = BinomialTree(6)

    one = one.merge(two)

    three = three.merge(four)
    six = five.merge(six)
    three = three.merge(six)

    one.neighbour_left = three
    asd = BinomialHeap(one)

    seven = BinomialTree(7)

    eight = BinomialTree(8)
    nine = BinomialTree(9)
    eight = eight.merge(nine)

    seven.neighbour_left = eight

    qwe = BinomialHeap(seven)

    qwe.merge(asd)
