# https://leetcode.com/problems/regular-expression-matching/submissions/1419425508


import math


debug = True


def solution(s: str, p: str):
    qwe = []
    for i in p:
        if i == '*':
            qwe[-1] = qwe[-1] + i
        else:
            qwe.append(i)
    print(qwe)
    if len(qwe) == len(p) and len(qwe) != len(s):
        return False

    n = len(s) + 1
    m = len(qwe) + 1
    table = [[math.inf] * n for _ in range(m)]

    a = 1
    table[0] = [a] * n
    table[0][0] = 0

    for i in range(1, m):
        table[i][0] = a

    if len(qwe[0]) == 2 or qwe[0] == '.' or qwe[0] == s[0]:
        table[1][1] = 0
    else:
        table[1][1] = a

    for i in range(1, m):
        patter = qwe[i - 1]
        for j in range(1, n):
            char = s[j - 1]

            if len(patter) == 2:  # if "?*"
                # print(i, j, patter)
                table[i][j] = min(table[i - 1][j - 1] + int(char != patter[0] and patter[0] != '.'),
                                  table[i - 1][j],
                                  table[i][j - 1] + int(char != patter[0] and patter[0] != '.'))
            elif patter == ".":
                table[i][j] = min(table[i - 1][j - 1],
                                  table[i - 1][j])
            else:
                # print(i, j, patter, char)
                if i == 1:
                    table[i][j] = table[i - 1][j] + int(patter != char and patter != '.')
                else:
                    table[i][j] = table[i - 1][j - 1] + int(patter != char and patter != '.')
    print(*table, sep='\n')
    return table[-1][-1] == 0


def solution2(s: str, p: str):
    qwe = []
    for i in p:
        if i == '*':
            qwe[-1] = qwe[-1] + i
        else:
            qwe.append(i)

    if len(qwe) == len(p) and len(qwe) != len(s):
        return False

    if len(qwe[0]) < 2 and qwe[0] != "." and qwe[0] != s[0]:
        return False

    n = len(s)
    m = len(qwe)
    table = [[0] * n for _ in range(m)]

    flag = qwe[0] == s[0]
    control = (len(qwe[0]) == 2 and qwe[0][0] != '.' and qwe[0][0] != s[0])

    for i in range(1, n):
        pattern = qwe[0]
        fp = pattern[0]
        target = s[i]

        if pattern == '.':
            table[0][i] = table[0][i - 1] + 1
        elif len(pattern) == 2:
            table[0][i] = table[0][i - 1] + int(target != fp and fp != '.') + control
            control = 0
        else:
            table[0][i] = table[0][i - 1] + int(target != fp or table[0][i - 1] != 0 or flag)
            if target == fp:
                flag = True

    flag = qwe[0] == s[0]
    count_point = qwe[0] == '.'

    for i in range(1, m):
        pattern = qwe[i]
        fp = pattern[0]
        target = s[0]

        if pattern == '.':
            table[i][0] = table[i - 1][0] + int(table[i - 1][0] != 0 or count_point)
            count_point += 1
        elif len(pattern) == 2:
            table[i][0] = table[i - 1][0]
        else:
            table[i][0] = table[i - 1][0] + int(target != fp or table[i - 1][0] != 0 or flag)
            if target == fp:
                flag = True

    for i in range(1, m):
        pattern = qwe[i]
        fp = pattern[0]
        for j in range(1, n):
            target = s[j]

            if len(pattern) == 2:  # if pattern == "?*"
                table[i][j] = min(table[i - 1][j],
                                  table[i][j - 1] + int(fp != target and fp != '.'))
            elif pattern == '.':
                table[i][j] = table[i - 1][j - 1]
            else:  # if char
                table[i][j] = table[i - 1][j - 1] + int(fp != target)

    if debug:
        print("  ", *s, sep='  ')
        for i in range(len(table)):
            print(qwe[i].center(2, ' '), table[i])
    return table[-1][-1] == 0


def test_1():
    s = "abccd"
    p = "a*.c*d"
    assert solution2(s, p)


def test_2():
    s = "aa"
    p = "a"
    assert not solution2(s, p)


def test_3():
    s = "aa"
    p = "a*"
    assert solution2(s, p)


def test_4():
    s = "cdaap"
    p = "a*b*a*cda*p*...a*"
    assert solution2(s, p)


def test_5():
    s = "cdaap"
    p = "a*b*cda*p*...p*"
    assert solution2(s, p)


def test_6():
    s = "cdaap"
    p = "a*b*a*cda*p*..da*"
    assert not solution2(s, p)


def test_7():
    s = "abcd"
    p = "d*"
    assert not solution2(s, p)


def test_8():
    s = "aab"
    p = "c*a*b"
    assert solution2(s, p)


def test_9():
    s = "aaa"
    p = "ab*a"
    assert not solution2(s, p)


def test_10():
    s = "abcdede"
    p = "ab.*de"
    assert solution2(s, p)


def test_11():
    s = "a"
    p = "b"
    assert not solution2(s, p)


def test_12():
    s = "aa"
    p = "b"
    assert not solution2(s, p)


def test_13():
    s = "a"
    p = "ab"
    assert not solution2(s, p)


def test_14():
    s = "aa"
    p = "ab"
    assert not solution2(s, p)


def test_15():
    s = "aa"
    p = "a"
    assert not solution2(s, p)


def test_16():
    s = "abb"
    p = "b*"
    assert not solution2(s, p)


if __name__ == "__main__":
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
    test_7()
    test_8()
    test_9()
    test_10()
    test_11()
    test_12()
    test_13()
    test_14()
    test_15()
    test_16()
