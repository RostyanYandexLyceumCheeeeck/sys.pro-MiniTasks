# https://leetcode.com/problems/trim-a-binary-search-tree/submissions/1220502519
# Решение на литкоде почти такое же, только там свой класс нельзя было использовать((

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class MyTreeNodeBST(TreeNode):
    def __init__(self, val=0, left=None, right=None, father=None):
        super().__init__(val, left, right)
        self.father = father

    def remove(self):
        baby = self.get_leftmost_of_right() if self.left and self.right \
            else self.left if self.left \
            else self.right if self.right \
            else None
        # baby = None
        # if self.left and self.right:
        #     baby = self.get_leftmost_of_right()
        # elif self.left:
        #     baby = self.left
        # elif self.right:
        #     baby = self.right
        self.linking_grandfather_and_grandson(baby)

    def get_leftmost_of_right(self):
        root = self.right
        while root.left:
            root = root.left
        return root

    def linking_grandfather_and_grandson(self, baby):
        if self.father.left == self:
            self.father.left = baby
        else:
            self.father.right = baby
        if baby:
            baby.father = self.father


class Solution:
    def trimBST(self, root: MyTreeNodeBST | None, low: int, high: int) -> MyTreeNodeBST | None:
        if root is None:
            return None

        if root.val < low:
            return self.trimBST(root.right, low, high)
        elif root.val > high:
            return self.trimBST(root.left, low, high)

        self.support_trimBST(root.left, low, high)
        self.support_trimBST(root.right, low, high)
        return root

    def support_trimBST(self, root: MyTreeNodeBST | None, low, hight):
        if root is None:
            return

        if root.val < low:
            root.left = None
            root.remove()
        elif root.val > hight:
            root.right = None
            root.remove()

        self.support_trimBST(root.left, low, hight)
        self.support_trimBST(root.right, low, hight)


if __name__ == "__main__":
    root = MyTreeNodeBST(3)
    root.left = MyTreeNodeBST(1, father=root)
    root.right = MyTreeNodeBST(4, father=root)
    root.left.right = MyTreeNodeBST(2, father=root.left)

    asd = Solution()
    asd.trimBST(root, 3, 4)
    print()


"""
[3,1,4,null,2] 3, 4

     ╔═══════3═══════╗
     1═══╗   |       4   
     |   2   |
"""