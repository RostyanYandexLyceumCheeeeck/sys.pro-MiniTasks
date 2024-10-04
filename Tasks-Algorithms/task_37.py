# https://leetcode.com/problems/unique-binary-search-trees/submissions/1411280703


def count_i(arr, n: int):
    result = 2 * (arr[n - 1] + arr[n - 2])
    for i in range(2, (n + 1) // 2):
        result += 2 * arr[i] * arr[n - i - 1]

    if n % 2:
        result -= arr[n//2] ** 2
    return result


def solution(n):
    arr = [0, 1, 2]
    if n <= 2:
        return arr[n]

    for i in range(3, n + 1):
        arr.append(count_i(arr, i))

    return arr[n]


def test():
    # arr = [0, 1, 2, 5, 14, 42, 132]
    assert 429 == solution(7)


if __name__ == "__main__":
    for j in range(8):
        print(solution(j))
    # test()
