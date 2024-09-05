# https://leetcode.com/problems/jump-game/submissions/1379845362


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        if len(nums) == 1:
            return True

        m = 0
        t = 0
        k = 0
        for i in range(len(nums) + 1):
            if i > m:
                return False

            k = i + nums[i]
            t = (k > m)
            m = t * k + m * (not t)
            if m >= len(nums) - 1:
                return True
