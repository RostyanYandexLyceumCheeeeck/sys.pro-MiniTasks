L = list[int]


def long_addition(x: L, y: L, jx: int = 0, lx: int = 0, jy: int = 0, ly: int = 0, ky: int = 1, qwe: int = 0) -> L:
    if ly > lx:
        return long_addition(y, x, jy, ly, jx, lx, ky)
    if debug:
        print(f"{'  '*qwe} long_addition!")
        print('  '*qwe, x, jx, lx)
        print('  '*qwe, y, jy, ly)
    res = []
    ym = 0
    for i in range(ly):
        temp = x[jx - i - 1] + y[jy - i - 1] * ky + ym
        ym = temp // 10
        res.append((temp + 10) % 10)

    for i in range(lx - ly):
        temp = x[jx - ly - i - 1] + ym
        ym = temp // 10
        res.append((temp + 10) % 10)

    if ym:
        res.append((10 + ym) % 10)
    if debug:
        print('  '*qwe, f"{res = }")
    while len(res) > 1 and not res[-1]:
        res.pop()
    return res[::-1]


def karatsuba(x: L, y: L, ix: int = 0, jx: int | None = 0, iy: int = 0, jy: int | None = 0, qwe: int = 0) -> L:
    lx, ly = jx - ix, jy - iy
    if ly > lx:
        return karatsuba(y, x, iy, jy, ix, jx, qwe)
    if debug:
        print()
        print('  '*qwe, x, ix, jx, lx)
        print('  '*qwe, y, iy, jy, ly)
    if (not lx) or (not ly):
        return [0]
    if lx == 1 == ly:
        p = x[ix] * y[iy]
        return [p] if p < 10 else [p // 10, p % 10]

    half_lx = lx // 2
    temp = half_lx + lx % 2

    if ly <= temp:                                                                                       #     123456789
        ac = []                                                                                          #         12345
        bd = karatsuba(x, y, ix + half_lx, jx, iy, jy, qwe + 1)                                          # -------------
        t1 = long_addition(x, x, jx, temp, ix + half_lx, lx - temp, qwe=qwe)                             #  1234 | 56789
        ba_dc = karatsuba(t1, y, 0, len(t1), iy, jy, qwe + 1)                                            #       | 12345

    else:                                                                                                #     123456789
        ac = karatsuba(x, y, ix, ix + half_lx, iy, jy - temp, qwe + 1)                                   #       1234567
        bd = karatsuba(x, y, ix + half_lx, jx, jy - temp, jy, qwe + 1)                                   # -------------
        t1 = long_addition(x, x, jx, temp, ix + half_lx, lx - temp, qwe=qwe)
        t2 = long_addition(y, y, jy, temp, jy - temp, ly - temp, qwe=qwe)                                #  1234 | 56789
        ba_dc = karatsuba(t1, t2, 0, len(t1), 0, len(t2), qwe + 1)                                       #    12 | 34567

    ba_dc_SUB_ac = long_addition(ba_dc, ac, 0, len(ba_dc), 0, len(ac), -1, qwe=qwe)
    step4 = long_addition(ba_dc_SUB_ac, bd, 0, len(ba_dc_SUB_ac), 0, len(bd), -1, qwe=qwe)
    if debug:
        print(f"{'  '*qwe}{step4 = }")
        print(f"{'  '*qwe}   {ac = }")
        print(f"{'  '*qwe}   {bd = }")
        print(f"{'  '*qwe}{ba_dc = }")
    for _ in range(temp):
        step4.append(0)
        ac.append(0)
    for _ in range(temp):
        ac.append(0)

    new_ac_add_new_step4 = long_addition(ac, step4, 0, len(ac), 0, len(step4), qwe=qwe)
    return long_addition(new_ac_add_new_step4, bd, 0, len(new_ac_add_new_step4), 0, len(bd), qwe=qwe)


def start_karatsuba(a: int, b: int, qwe: int = 0) -> int:
    sign = -1 if a < 0 else 1
    sign *= -1 if b < 0 else 1
    a, b = abs(a), abs(b)

    if debug:
        print(f"========={a, b}")
    x = list(map(int, str(a)))
    y = list(map(int, str(b)))

    res_arr = karatsuba(y, x, 0, len(y), 0, len(x), qwe) \
        if len(x) < len(y) else \
        karatsuba(x, y, 0, len(x), 0, len(y), qwe)
    return sign * int("".join(map(str, res_arr)))


def initial_tests(func, tests):
    global debug
    for i, j in tests:
        a, b = i * j, start_karatsuba(i, j)
        try:
            assert a == b
        except:
            print(f"{i = }; {j = }\n{a = }; {b = }\n")
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
    # print(long_addition([1, 2, 3, 5], [8, 7, 6, 5], 0, 4, 0, 4))
    if not debug:
        base_test()
        autor_test()
    else:
        print(start_karatsuba(10, 10))


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
