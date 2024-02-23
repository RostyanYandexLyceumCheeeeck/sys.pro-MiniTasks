# https://leetcode.com/problems/global-and-local-inversions/submissions/1184345748

def inversion(arr: list[int]):
    el, j = arr[0], 0
    m, k = el, j
    for i in range(len(arr)):
        if i - j > 1 and el > arr[i]:
            return False
        if i - k > 1 and m > arr[i]:
            return False

        if arr[i] > el:
            m, k = el, j
            el, j = arr[i], i
    return True


if __name__ == "__main__":
    mas = [1, 2, 0]
    print(inversion(mas))
