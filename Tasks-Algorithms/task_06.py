# https://leetcode.com/problems/wiggle-sort-ii/submissions/1211137688
from task_05 import recurs_shellsort


def wiggleSort(arr: list):
    recurs_shellsort(arr)
    if len(arr) < 3:
        return

    middle = len(arr) // 2
    ost = len(arr) % 2
    res = []
    temp = middle
    middle += len(arr) % 2

    for i in range(temp):
        res.append(arr[middle - 1 - i])
        res.append(arr[-1 - i])

    if temp != middle:
        res.append(arr[0])
    arr[:] = res[:]


def test(qwe):
    print(qwe)
    wiggleSort(qwe)
    print(qwe)
    print()


if __name__ == "__main__":
    test([1,4,3,4,1,2,1,3,1,3,2,3,3])
    asd = [1, 5, 1, 1, 6, 4, 1, 7]
    zxc = [1, 5, 1, 1, 6, 4]
    test([3, 1, 1, 4, 1, 1, 1, 3, 3])
    test([1, 5, 1, 1, 6, 4, 1, 7, 1, 8, 1])
    test([1, 5, 1, 1, 6, 4, 1, 7, 1, 8])
    test(asd)
    test(zxc)
    test([1, 3, 2, 2, 3, 1])
