# https://leetcode.com/problems/serialize-and-deserialize-binary-tree/submissions/1220384639

# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        res = self.support_serialize(root)
        return "".join(res[1:-1] if res else res)

    def support_serialize(self, root, result: list | None = None):
        if not result:
            result = []
        if not root:
            if result:
                result.append('x')
            return result
        result.append('(')
        result.append(str(root.val))

        self.support_serialize(root.left, result)
        self.support_serialize(root.right, result)

        result.append(')')
        return result

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        if not len(data):
            return None

        return self.support_deserialize([data])[0]

    def support_deserialize(self, lst_data: list[str], start: int = 0):
        data = lst_data[0]
        last = i = start
        n = 0
        babies = [None, None]
        while i < len(data):
            if data[i] == 'x':
                n += 1
            elif data[i] == '(':
                babies[n], i = self.support_deserialize(lst_data, i + 1)
                n += 1
            elif data[i] == ')':
                break
            i += 1

        while data[last] not in 'x()':
            last += 1

        value = data[start:last]
        res = TreeNode(int(value))
        res.left = babies[0]
        res.right = babies[1]
        return res, i

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))


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
    ans = Codec()
    qwe = ans.serialize(root)
    print(qwe)
    print(ans.serialize(ans.deserialize(qwe)))
    print(ans.deserialize(''))

"""
     ╔═══════0═══════╗
 ╔═══1       |   ╔═══3═══╗   
 2   |       | ╔═4═╗ |   7═╗
             | 5 | 6 |   | 8
"""
"""
0(1(2xx)x)(3(4(5xx)(6xx))(7x(8xx)))
0(1(2xx)x)(3(4(5xx)(6xx))(7x(8xx)))
None
╔
╗
═
"""
