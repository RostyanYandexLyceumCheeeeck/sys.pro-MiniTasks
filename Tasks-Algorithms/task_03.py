#  https://leetcode.com/problems/binary-search/submissions/1173352735
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums)
        k = (r + l) // 2
        while l < k < r:
            if nums[k] == target:
                return k
            if nums[k] < target:
                l = k
            else:
                r = k
            k = (r + l) // 2
        if nums[k] == target:
            return k
        return -1


if __name__ == "__main__":
    k = 5
    for i in range(10):
        print(i, end=' ')
        i = min(i, k)
        print(i, k)