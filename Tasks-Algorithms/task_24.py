# https://leetcode.com/problems/validate-binary-search-tree/submissions/1220452171
from math import inf


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        return self.supportIsValidBST(root)

    def supportIsValidBST(self, root, start=-inf, end=inf) -> bool:
        if root is None:
            return True

        if not (start < root.value < end):
            return False

        return self.supportIsValidBST(root.left, start, root.value) and \
            self.supportIsValidBST(root.right, root.value, end)


