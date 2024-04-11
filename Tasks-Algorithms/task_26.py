# https://leetcode.com/problems/balance-a-binary-search-tree/submissions/1229790506

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def balanceBST(self, root: TreeNode):
        return self.arr_to_tree(self.tree_to_arr(root))

    def arr_to_tree(self, arr, l: int = 0, r: int | None = None):
        if r is None:
            r = len(arr)

        if r - l == 3:
            return TreeNode(arr[l + 1], TreeNode(arr[l]), TreeNode(arr[l + 2]))
        if r - l == 2:
            return TreeNode(arr[l + 1], TreeNode(arr[l]))
        if r - l == 1:
            return TreeNode(arr[l])

        mid = (l + r) // 2
        return TreeNode(arr[mid], self.arr_to_tree(arr, l, mid), self.arr_to_tree(arr, mid + 1, r))

    def tree_to_arr(self, root: TreeNode | None = None, result: list | None = None):
        if result is None:
            result = list()

        if root is None:
            return result

        self.tree_to_arr(root.left, result)
        result.append(root.val)
        self.tree_to_arr(root.right, result)
        return result


def test1():  # [1,null,2,null,3,null,4]
    root = TreeNode(1)                    # . 1══╗                                           ╔══3══╗
    root.right = TreeNode(2)              # . |  2══╗                      ========\      ╔══2  |  4
    root.right.right = TreeNode(3)        # . |  |  3══╗                   ========/      1  |  |
    root.right.right.right = TreeNode(4)  # . |  |  |  4

    res = Solution()
    qwe = res.balanceBST(root)
    print(qwe)  # point debug


def test2():  # [19,10,null,4,17,null,5]
    root = TreeNode(19)                   # .     ╔═══════19                             ╔══10═════╗
    root.left = TreeNode(10)              # . ╔═══10═══╗   |               ========\   ╔═5   | ╔══19
    root.left.left = TreeNode(4)          # . 4═╗  |   17  |               ========/   4 |   | 17  |
    root.left.right = TreeNode(17)        # . | 5  |       |
    root.left.left.right = TreeNode(5)    # .

    res = Solution()
    qwe = res.balanceBST(root)
    print(qwe)  # point debug


def test3():  # [1,null,15,14,17,7,null,null,null,2,12,null,3,9,null,null,null,null,11]
    root = TreeNode(1)                    # . 1═══════════════════╗
    l2 = root.right = TreeNode(15)        # . |              ╔════15═══╗                    ╔════11════════╗
    l2.right = TreeNode(17)               # . |      ╔══════14    |   17   ========\     ╔══7══╗ |     ╔══15══╗
    l3 = l2.left = TreeNode(14)           # . | ╔════7════╗  |    |        ========/   ╔═2  |  9 |  ╔═14   | 17
    l4 = l3.left = TreeNode(7)            # . | 2═══╗|╔═══12 |    |                    1 |  |    |  12 |   |
    l4.left = TreeNode(2)                 # . | |   3|9═╗  | |    |
    l5 = l4.right = TreeNode(12)          # . | |    || 11 | |    |
    l5.left = TreeNode(9)
    l5.left.right = TreeNode(11)

    res = Solution()
    qwe = res.balanceBST(root)
    print(qwe)  # point debug


if __name__ == "__main__":
    test1()
    test2()
    test3()

"""
        ╔════11════════╗
     ╔══7══╗ |     ╔══15══╗
   ╔═2  |  9 |  ╔═14   | 17
   1 |  |    |  12 |   |
"""