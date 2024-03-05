from random import randint, shuffle


def control(func):
    def posrednik(arr: list[tuple[int, int]], start: int = 0, end: int | None = None, pos: int | None = None):
        if len(arr) < 2:
            return arr[0]

        if end is None:
            end = len(arr)

        if end - start < 2:
            return arr[start]

        if pos is None:
            pos = (start + end) // 2
        return func(arr, start, end, pos)
    return posrednik


@control
def quick_search(arr: list[tuple[int, int]], start: int, end: int, pos: int):
    temp = randint(start, end - 1)
    target = arr[temp][1]
    # print(arr)
    # print(start, end, temp, target, pos)
    arr[temp], arr[start] = arr[start], arr[temp]
    i, k = start, start

    for j in range(start + 1, end):
        if arr[j][1] < target:
            arr[j], arr[k + 1], arr[i] = arr[k + 1], arr[i], arr[j]
            i += 1
            k += 1
        elif arr[j][1] == target:
            arr[k + 1], arr[j] = arr[j], arr[k + 1]
            k += 1
    # print(start, end, temp, target, pos, i, k)
    # print(arr)
    # print()
    p = i + 1 - start
    if p == pos:
        return arr[p - 1 + start]
    elif p > pos:
        return quick_search(arr, start, i, pos)
    else:
        return quick_search(arr, k + 1, end, pos - p)


def test1():
    qwe = [(0, y) for y in range(1000)]
    for x in range(10000):
        shuffle(qwe)
        res = quick_search(qwe, pos=500)
        assert 499 <= res[1] <= 500


if __name__ == "__main__":
    test1()
