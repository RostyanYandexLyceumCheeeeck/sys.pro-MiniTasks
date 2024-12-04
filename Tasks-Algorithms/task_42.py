from random import random


class Root:
    def __init__(self, index: int, priority=None, value=0):
        self.count = 1
        self.key = index
        self.val = value
        self.summary = value
        self.father = None
        self.priority = priority if priority else random()

        self.left = None
        self.right = None

    def set_left(self, left=None):
        self.left = left
        if left:
            left.father = self
        self.update()

    def set_right(self, right=None):
        self.right = right
        if right:
            right.father = self
        self.update()

    def pop_left(self):
        res = self.left
        if self.left:
            self.left.father = None
            self.left = None
        self.update()
        return res

    def pop_right(self):
        res = self.right
        if self.right:
            self.right.father = None
            self.right = None
        self.update()
        return res

    def update(self):
        self.count = 1
        self.summary = self.val
        if self.left:
            self.count += self.left.count
            self.summary += self.left.summary
        if self.right:
            self.count += self.right.count
            self.summary += self.right.summary

    def update_rec(self):
        if self.left:
            self.left.update_rec()
        if self.right:
            self.right.update_rec()
        self.update()

    @staticmethod
    def merge(root1, root2):
        if not root1:
            return root2
        if not root2:
            return root1

        if root1.priority < root2.priority:
            # root1.count += root2.count
            root1.set_right(Root.merge(root1.right, root2))
            root1.update()
            return root1

        # root2.count += root1.count
        root2.set_left(Root.merge(root1, root2.left))
        root2.update()
        return root2

    def to_arr(self, result: list = None):
        if result is None:
            result = []

        if self.left:
            self.left.to_arr(result)
        result.append(self.val)
        if self.right:
            self.right.to_arr(result)
        return result


class ImTreap:
    def __init__(self, root=None):
        self.root = root

    def sort_arr_to_imtreap(self, arr: list):
        if not arr:
            return

        last = self.root = Root(*arr[0])
        for i in range(1, len(arr)):
            target = Root(*arr[i])
            while last and target.priority < last.priority:
                last = last.father

            if last:
                target.set_left(last.pop_right())
                last.set_right(target)
                target.update()
                last.update()
            else:
                target.set_left(self.root)
                self.root = target
                self.root.update()
            last = target
        self.root.update_rec()

    @staticmethod
    def merge(imt1, imt2):
        if not imt1 or not imt1.root:
            return imt2
        if not imt2 or not imt2.root:
            return imt1

        Root.merge(imt1.root, imt2.root)
        if imt1.root.priority < imt2.root.priority:
            return imt1
        return imt2

    @staticmethod
    def split_by_size(imt, k):
        if not imt:
            return None, None
        if k <= 0:
            return None, imt
        if k >= imt.root.count:
            return imt, None

        cl = imt.root.left.count if imt.root.left else 0

        if k <= cl:
            ll, lr = ImTreap.split_by_size(ImTreap(imt.root.left), k)
            imt.root.set_left(lr.root if lr else lr)
            imt.root.update()

            ll.root.father = None
            imt.root.father = None
            return ll, imt

        rl, rr = ImTreap.split_by_size(ImTreap(imt.root.right), k - cl - 1)
        imt.root.set_right(rl.root if rl else rl)
        imt.root.update()

        imt.root.father = None
        if rr and rr.root:
            rr.root.father = None
        return imt, rr

    @staticmethod
    def insert(imt, val, pos, priority=None):
        center = ImTreap(Root(pos, priority, val))
        return ImTreap.__insert_many(imt, pos, center)

    @staticmethod
    def __insert_many(imt, pos, center):
        left, right = ImTreap.split_by_size(imt, pos)
        return ImTreap.merge(ImTreap.merge(left, center), right)

    @staticmethod
    def erase(imt, pos, count=1, flag_get_del=False):
        if count <= 0:
            return imt

        left, right = ImTreap.split_by_size(imt, pos)
        rl, rr = ImTreap.split_by_size(right, count)
        res = ImTreap.merge(left, rr)

        if flag_get_del:
            return res, rl
        return res

    @staticmethod
    def sum(imt, start, end):
        if not imt or not imt.root:
            return 0

        full = imt.root.summary
        left, center = ImTreap.erase(imt, start, end - start + 1, True)
        result = full - (left.root.summary if left and left.root else 0)

        ImTreap.__insert_many(left, start, center)
        return result

    def imtreap_to_arr(self, result: list = None):
        return self.root.to_arr(result)


def test1():
    arr = [
        [0, 10, 8],
        [1, 8, 12],
        [2, 14, 14],
        [3, 4, 15],
        [4, 9, 18],
        [5, 6, 23],
        [6, 15, 24],
        [7, 11, 25],
    ]

    qwe = ImTreap()
    qwe.sort_arr_to_imtreap(arr)
    assert qwe.imtreap_to_arr() == [x[-1] for x in arr]


def test2():
    arr = [
        [0, 10, 8],
        [1, 8, 12],
        [2, 14, 14],
        [3, 4, 15],
        [4, 9, 18],
        [5, 6, 23],
        [6, 15, 24],
        [7, 11, 25],
    ]
    k = 2

    qwe = ImTreap()
    qwe.sort_arr_to_imtreap(arr)
    asd, zxc = ImTreap.split_by_size(qwe, k)
    assert asd.imtreap_to_arr() == [x[-1] for x in arr[:k]]
    assert zxc.imtreap_to_arr() == [x[-1] for x in arr[k:]]


def test3():
    arr = [
        [0, 10, 8],
        [1, 8, 12],
        [2, 14, 14],
        [3, 4, 15],
        [4, 9, 18],
        [5, 6, 23],
        [6, 15, 24],
        [7, 11, 25]
    ]

    one = [3, 16, 13]
    two = [6, 89, 77]

    qwe = ImTreap()
    qwe.sort_arr_to_imtreap(arr)
    qwe.insert(qwe, one[-1], one[0], one[1])
    qwe.insert(qwe, two[-1], two[0], two[1])

    first, second = ImTreap.split_by_size(qwe, one[0] + 1)
    answer_first = [x[-1] for x in (arr[:one[0]] + [one])]
    answer_second = [
        x[-1] for x in (
                arr[one[0]:two[0] - 1] + [two] + arr[two[0] - 1:]
            )
        ]
    # print(answer_first)
    # print(first.imtreap_to_arr())
    # print(answer_second)
    # print(second.imtreap_to_arr())

    assert first.imtreap_to_arr() == answer_first
    assert second.imtreap_to_arr() == answer_second


def test4():
    arr = [
        [0, 10, 8],
        [1, 8, 12],
        [2, 14, 14],
        [3, 4, 15],
        [4, 9, 18],
        [5, 6, 23],
        [6, 15, 24],
        [7, 11, 25],
    ]
    k = 2

    qwe = ImTreap()
    qwe.sort_arr_to_imtreap(arr)
    asd, zxc = ImTreap.split_by_size(qwe, k)
    assert asd.root.summary == sum(x[-1] for x in arr[:k])
    assert zxc.root.summary == sum(x[-1] for x in arr[k:])

    save_c_asd = asd.root.count
    save_c_zxc = zxc.root.count

    assert save_c_asd == k
    assert save_c_zxc == len(arr) - k

    def check_sum(imt, save_c_imt, shift=0):
        for start in range(save_c_imt):
            for end in range(start, save_c_imt):
                assert ImTreap.sum(imt, start, end) == sum(x[-1] for x in arr[start + shift:end + shift + 1])
        assert imt.root.count == save_c_imt

    check_sum(asd, save_c_asd)
    check_sum(zxc, save_c_zxc, k)


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
