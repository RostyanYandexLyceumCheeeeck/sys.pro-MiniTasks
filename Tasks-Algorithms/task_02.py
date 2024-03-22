L = list[int, ...]


def long_addition(x: L, y: L, jx: int = 0, lx: int = 0, jy: int = 0, ly: int = 0, qwe: int = 0) -> int:
    if debug:
        print(f"{qwe} long_addition!")
        print(x, jx, lx)
        print(y, jy, ly)
    summa = 0
    k = 1
    ym = 0
    for i in range(ly):
        temp = x[jx - i - 1] + y[jy - i - 1] + ym
        ym = temp // 10
        summa += (temp % 10) * k
        k *= 10

    for i in range(lx - ly):
        temp = x[jx - ly - i - 1] + ym
        ym = temp // 10
        summa += (temp % 10) * k
        k *= 10
    summa += ym * k
    if debug:
        print(f"{summa = }")
    return summa


def karatsuba(x: L, y: L, ix: int = 0, jx: int = 0, iy: int = 0, jy: int = 0, qwe: int = 0) -> int:
    lx, ly = jx - ix, jy - iy
    if debug:
        print()
        print(qwe, x, ix, jx, lx)
        print(qwe, y, iy, jy, ly)
    if lx == 1 == ly:
        return x[ix] * y[iy]

    half_lx = lx // 2
    temp = half_lx + lx % 2

    if ly <= temp:                                                                                       #     123456789
        ac = 0                                                                                           #         12345
        bd = karatsuba(x, y, ix + half_lx, jx, iy, jy, qwe + 1)                                          # -------------
        ba_dc = start_karatsuba(long_addition(x, x, jx, temp, ix + half_lx, lx - temp, qwe),             #  1234 | 56789
                                long_addition(y, [], jy, ly, 0, 0, qwe), qwe + 1)                        #       | 12345

    else:                                                                                                #     123456789
        ac = karatsuba(x, y, ix, ix + half_lx, iy, jy - temp, qwe + 1)                                   #       1234567
        bd = karatsuba(x, y, ix + half_lx, jx, jy - temp, jy, qwe + 1)                                   # -------------
        ba_dc = start_karatsuba(long_addition(x, x, jx, temp, ix + half_lx, lx - temp, qwe),             #  1234 | 56789
                                long_addition(y, y, jy, temp, jy - temp, ly - temp, qwe), qwe + 1)       #    12 | 34567
    step4 = ba_dc - ac - bd
    if debug:
        print(f"{qwe}{step4 = }")
        print(f"{qwe}   {ac = }")
        print(f"{qwe}   {bd = }")
        print(f"{qwe}{ba_dc = }")
    return (ac * 10 ** (2 * temp)) + (step4 * 10 ** temp) + bd


def start_karatsuba(a: int, b: int, qwe: int = 0) -> int:
    sign = -1 if a < 0 else 1
    sign *= -1 if b < 0 else 1
    a, b = abs(a), abs(b)

    if debug:
        print(f"========={a, b}")
    x = list(map(int, str(a)))
    y = list(map(int, str(b)))
    return sign * (karatsuba(y, x, 0, len(y), 0, len(x), qwe)
                   if len(x) < len(y) else
                   karatsuba(x, y, 0, len(x), 0, len(y), qwe))


def initial_tests(func, tests):
    global debug
    for i, j in tests:
        a, b = i * j, start_karatsuba(i, j)
        try:
            assert a == b
        except:
            print(f"{i = }\n, {j = }\n, {a = }\n, {b = }\n")
            debug = True
            print(func(i, j))
            exit(0)


def base_test():
    initial_tests(start_karatsuba, [(j, i) for i in range(1025) for j in range(1025)])
    print("base_tests out!")


def autor_test():
    tests_0 = [
        (12356789098765432123456789876543212345676543, 12),
        (12356789098765432123456789876543212345676543, -12),
        (-12356789098765432123456789876543212345676543, -12),
        (12, 12356789098765432123456789876543212345676543),
        (123, 12356789098765432123456789876543212345676543),
        (12, 123567890987654321234567898765432123456765430),
        (123, 123567890987654321234567898765432123456765430),
        (12356789098765432123456789876543212345676549, 12356789098765432123456789876543212345676543),
        (12356789098765432123456789876543212345676540, 12356789098765432123456789876543212345676543),
    ]
    initial_tests(start_karatsuba, tests_0)
    print("autor_tests №0 out!")


if __name__ == "__main__":
    debug = False
    if not debug:
        base_test()
        autor_test()
    else:
        print(start_karatsuba(100, 100))


"""
    123456789
        12345
-------------
 1234 | 56789
      | 12345
=============
    123456789
      1234567
-------------
 1234 | 56789
   12 | 34567
=============



1234567
5

123 4567

"""
