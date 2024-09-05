# https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/submissions/1379855937


def solution(arr):
    if not arr:
        return 0

    last_cell = 0
    last_buy = arr[0]
    res = -last_buy

    for i in range(1, len(arr)):
        if arr[i] <= last_buy:
            res += last_buy
            res -= arr[i]
            last_buy = arr[i]
            last_cell = 0
        elif arr[i] >= last_cell:
            res -= last_cell
            res += arr[i]
            last_cell = arr[i]
            last_buy = 0
        else:
            res -= arr[i]
            last_buy = arr[i]
            last_cell = 0
    return res + last_buy


if __name__ == "__main__":
    print(solution(list(map(int, input().split()))))
