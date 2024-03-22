L = list[int, ...]


def check(x: L, y: L, shift: int = 0) -> bool:
    if len(x) < len(y) + shift:
        return False

    res = 0
    for i in range(len(y) - 1, -1, -1):
        res = 0 if x[i + shift] >= y[i] + res else 1
    if not shift:
        return not bool(res)

    for i in range(shift - 1, -1, -1):
        if x[i] >= res:
            return True
    return not bool(res)


def long_difference(x: L, y: L, shift: int = 0) -> None:
    for i in range(len(y) - 1, -1, -1):
        j = i + shift
        x[j] -= y[i]
        if x[j] < 0:
            x[j] += 10
            x[j - 1] -= 1


def long_division(x: L, y: L, res: L, shift: int = 0) -> L:
    if debug:
        print()
        print(x)
        print(y)
        print(res, shift)
    count = 0
    while check(x, y, shift):

        count += 1
        long_difference(x, y, shift)

    res.append(count)
    if debug:
        print(res)
        print(x)
    if len(x) <= len(y) + shift:
        return res
    return long_division(x, y, res, shift + 1)


def division(a: int, b: int) -> int:
    if not b:
        raise ZeroDivisionError

    sign = -1 if a < 0 else 1
    sign *= -1 if b < 0 else 1
    a, b = abs(a), abs(b)

    x = list(map(int, str(a)))
    y = list(map(int, str(b)))
    res = []
    long_division(x, y, res)

    summa = 0
    k = 1
    for i in range(-1, -len(res) - 1, -1):
        summa += res[i] * k
        k *= 10
    return sign * summa


def test():
    for j in range(1, 1025):
        for i in range(1025):
            a, b = i // j, division(i, j)
            assert a == b


if __name__ == "__main__":
    debug = False
    print(division(10, 2)) if debug else test()

