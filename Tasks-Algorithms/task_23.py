# https://leetcode.com/problems/binary-tree-right-side-view/submissions/1220429023

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rightSideView(self, root: TreeNode | None) -> list[int]:
        res, right_h = self.heightRight(root)
        return res

    def heightRight(self, root, height: int = 0, lim_h: int = -1, res: list | None = None):
        if res is None:
            res = []
        if root is None:
            return res, height

        if height > lim_h:
            res.append(root.val)

        # mh = height  # max height
        if root.right:
            lim_h = max(lim_h, self.heightRight(root.right, height + 1, lim_h, res)[1])
        if root.left:
            lim_h = max(lim_h, self.heightRight(root.left, height + 1, lim_h, res)[1])

        return res, max(lim_h, height)


if __name__ == "__main__":
    root = TreeNode(0)
    root.left = TreeNode(1)
    root.left.left = TreeNode(2)

    root.right = TreeNode(3)
    root.right.left = TreeNode(4)
    root.right.left.left = TreeNode(5)
    root.right.left.right = TreeNode(6)
    root.right.right = TreeNode(7)
    root.right.right.right = TreeNode(8)
    asd = Solution()
    print(asd.rightSideView(root))


"""
     ╔═══════0═══════╗
 ╔═══1       |   ╔═══3═══╗   
 2   |       | ╔═4═╗ |   7═╗
             | 5 | 6 |   | 8
"""