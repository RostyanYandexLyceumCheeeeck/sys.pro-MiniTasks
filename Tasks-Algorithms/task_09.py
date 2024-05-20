from random import randint, shuffle
from statistics import stdev, geometric_mean
import time
import pprint
from copy import copy


T = list[list[int]]
t = tuple[int, int]
lt = list[t, t]
ltN = lt | None
size_classic = 16


def base_test():
    qwe = [[1, 2, 3, 4, 5],
           [2, 3, 4, 5, 6],
           [5, 6, 7, 8, 9],
           [1, 1, 1, 1, 1],
           [2, 1, 4, 3, 6]]

    asd = [[1, 2, 3, 4, 5],
           [1, 2, 3, 4, 5],
           [1, 2, 3, 4, 5],
           [1, 2, 3, 4, 5],
           [1, 2, 3, 4, 5]]

    print(classic(qwe, asd))
    print(recursive(qwe, asd))
    print(start_Strassen(qwe, asd))


def test1():
    for n in range(1, 65):
        one, two = generate_test(n)

        res_classic = classic(one, two)
        res_recurse = recursive(one, two)
        res_Strassen = start_Strassen(one, two)
        assert res_classic == res_recurse == res_Strassen


def generate_test(n):
    basis = lambda _: [randint(-10000, 10000) for _ in range(n)]
    one = [basis(_) for _ in range(n)]
    two = [basis(_) for _ in range(n)]
    return one, two


def exec_time_algo(*args, algo=None):
    count_run = 5  # randint(3, 11)
    durations = []
    for i in range(count_run):
        ts = time.time()
        algo(*args)
        fs = time.time() - ts
        durations.append(fs)

    sample = sum(durations) / count_run
    standard = stdev(copy(durations))

    geometric = 1
    for i in durations:
        geometric *= i
    geometric = geometric ** (1/count_run)
    return sample, standard, geometric


def stand():
    global gg_end, size_classic

    bench = []
    algos = ["classic", "recursive", "Strassen", "size_classic"]
    results = [[]]

    name_bench = lambda x: f"size {x}x{x}"

    size = 1
    optional = 3
    funcs = [classic, recursive, Strassen]
    while optional:
        durations = []
        one, two = generate_test(size)
        for func in funcs:
            times_func = exec_time_algo(one, two, algo=func)
            durations.append(times_func)
            results[-1].append("  ".join([format(x, '.6f') for x in times_func]))
        results[-1].append(str(size_classic))
        results.append([])

        if all([durations[-1][i] < min(durations[0][i], durations[1][i]) for i in range(3)]):
            optional -= 1
        elif size > 256:
            size_classic <<= 1
        bench.append(name_bench(size))
        size <<= 1

    gg_end = time.time()
    results.pop()
    format_table(bench, algos, results)


def addition_matrix2(first_matrix: T, second_matrix: T, pointers: ltN = None, ends: ltN = None,
                     sign: int = 1, multi: int = 1) -> T:
    if pointers is None:
        pointers = [(0, 0), (0, 0)]
    if ends is None:
        ends = [(len(first_matrix), len(first_matrix[0])), (len(second_matrix), len(second_matrix[0]))]

    lns = [(ends[0][0] - pointers[0][0], ends[0][1] - pointers[0][1]),   # sizes first matrix
           (ends[1][0] - pointers[1][0], ends[1][1] - pointers[1][1])]   # sizes second matrix

    result = []
    for i in range(lns[0][0]):
        i_f, i_s = i + pointers[0][0], i + pointers[1][0]
        line = []

        for j in range(lns[0][1]):
            j_f, j_s = j + pointers[0][1], j + pointers[1][1]
            line.append(multi * (first_matrix[i_f][j_f] + sign * second_matrix[i_s][j_s]))
        result.append(line)
    return result


def addition_matrix(first_matrix: T, second_matrix: T, pointers: ltN = None, ends: ltN = None,
                    sign: int = 1, multi: int = 1) -> T:
    if pointers is None:
        pointers = [(0, 0), (0, 0)]
    if ends is None:
        ends = [(len(first_matrix), len(first_matrix[0])), (len(second_matrix), len(second_matrix[0]))]

    lns = [(ends[0][0] - pointers[0][0], ends[0][1] - pointers[0][1]),   # sizes first matrix
           (ends[1][0] - pointers[1][0], ends[1][1] - pointers[1][1])]   # sizes second matrix

    result = []
    for i in range(min(lns[0][0], lns[1][0])):
        i_f, i_s = i + pointers[0][0], i + pointers[1][0]
        line = []

        for j in range(min(lns[0][1], lns[1][1])):
            j_f, j_s = j + pointers[0][1], j + pointers[1][1]
            line.append(multi * (first_matrix[i_f][j_f] + sign * second_matrix[i_s][j_s]))

        line += [multi * sign * elem for elem in second_matrix[i_s][pointers[1][1] + lns[0][1]:]] \
            if lns[0][1] < lns[1][1] else \
            copy.copy(first_matrix[i_s][pointers[0][1] + lns[1][1]:ends[0][1]])
        result.append(line)

    for i in range(abs(lns[1][0] - lns[0][0])):
        result.append([multi * sign * elem for elem in second_matrix[pointers[1][0] + lns[0][0] + i][pointers[1][0]:ends[1][0]]]
                      if lns[0][0] < lns[1][0] else
                      copy.copy(first_matrix[pointers[0][0] + lns[1][0] + i][pointers[0][1]:ends[0][1]]))
        result[-1] += [0] * abs(lns[0][1] - lns[1][1])

    return result


def classic(first_matrix: T, second_matrix: T, pointers: ltN = None, ends: ltN = None) -> T:
    if pointers is None:
        pointers = [(0, 0), (0, 0)]
    if ends is None:
        ends = [(len(first_matrix), len(first_matrix[0])), (len(second_matrix), len(second_matrix[0]))]

    lns = [(ends[0][0] - pointers[0][0], ends[0][1] - pointers[0][1]),  # sizes first matrix
           (ends[1][0] - pointers[1][0], ends[1][1] - pointers[1][1])]  # sizes second matrix

    result = []
    for i in range(lns[0][0]):
        line = []
        for j in range(lns[1][1]):
            s = 0
            for k in range(min(lns[1][0], lns[0][1])):
                i_f, i_s = pointers[0][0] + i, pointers[1][0] + k
                j_f, j_s = pointers[0][1] + k, pointers[1][1] + j
                s += first_matrix[i_f][j_f] * second_matrix[i_s][j_s]
            line.append(s)
        result.append(line)
    return result


def recursive(first_matrix: T, second_matrix: T, pointers: ltN = None, ends: ltN = None) -> T:
    if pointers is None:
        pointers = [(0, 0), (0, 0)]
    if ends is None:
        ends = [(len(first_matrix), len(first_matrix[0])), (len(second_matrix), len(second_matrix[0]))]

    lns = [(ends[0][0] - pointers[0][0], ends[0][1] - pointers[0][1]),   # sizes first matrix
           (ends[1][0] - pointers[1][0], ends[1][1] - pointers[1][1])]   # sizes second matrix

    if min(lns[0]) <= size_classic or min(lns[1]) <= size_classic:
        return classic(first_matrix, second_matrix, pointers, ends)

    mids_i = [pointers[0][0] + lns[0][0] // 2, pointers[1][0] + lns[1][0] // 2]  # middles lines
    mids_j = [pointers[0][1] + lns[0][1] // 2, pointers[1][1] + lns[1][1] // 2]  # middles column

    # coords little matrix
    A = [pointers[0], (mids_i[0], mids_j[0])]
    B = [(pointers[0][0], mids_j[0]), (mids_i[0], ends[0][1])]
    C = [(mids_i[0], pointers[0][1]), (ends[0][0], mids_j[0])]
    D = [(mids_i[0], mids_j[0]), ends[0]]

    E = [pointers[1], (mids_i[1], mids_j[1])]
    F = [(pointers[1][0], mids_j[1]), (mids_i[1], ends[1][1])]
    G = [(mids_i[1], pointers[1][1]), (ends[1][0], mids_j[1])]
    H = [(mids_i[1], mids_j[1]), ends[1]]

    left_up = addition_matrix2(first_matrix=recursive(first_matrix, second_matrix,  # AE
                                                     pointers=[A[0], E[0]],
                                                     ends=[A[1], E[1]]),
                              second_matrix=recursive(first_matrix, second_matrix,  # BG
                                                      pointers=[B[0], G[0]],
                                                      ends=[B[1], G[1]]))

    left_bottom = addition_matrix2(first_matrix=recursive(first_matrix, second_matrix,  # CE
                                                         pointers=[C[0], E[0]],
                                                         ends=[C[1], E[1]]),
                                  second_matrix=recursive(first_matrix, second_matrix,  # DG
                                                          pointers=[D[0], G[0]],
                                                          ends=[D[1], G[1]]))

    right_up = addition_matrix2(first_matrix=recursive(first_matrix, second_matrix,  # AF
                                                      pointers=[A[0], F[0]],
                                                      ends=[A[1], F[1]]),
                               second_matrix=recursive(first_matrix, second_matrix,  # BH
                                                       pointers=[B[0], H[0]],
                                                       ends=[B[1], H[1]]))

    right_bottom = addition_matrix2(first_matrix=recursive(first_matrix, second_matrix,  # CF
                                                          pointers=[C[0], F[0]],
                                                          ends=[C[1], F[1]]),
                                   second_matrix=recursive(first_matrix, second_matrix,  # DH
                                                           pointers=[D[0], H[0]],
                                                           ends=[D[1], H[1]]))

    for i in range(len(left_up)):
        left_up[i] += right_up[i]
    for i in range(len(left_bottom)):
        left_bottom[i] += right_bottom[i]
    left_up += left_bottom

    return left_up


def Strassen(first_matrix: T, second_matrix: T, pointers: ltN = None, ends: ltN = None) -> T:
    if pointers is None:
        pointers = [(0, 0), (0, 0)]
    if ends is None:
        ends = [(len(first_matrix), len(first_matrix[0])), (len(second_matrix), len(second_matrix[0]))]

    lns = [(ends[0][0] - pointers[0][0], ends[0][1] - pointers[0][1]),   # sizes first matrix
           (ends[1][0] - pointers[1][0], ends[1][1] - pointers[1][1])]   # sizes second matrix

    if min(lns[0]) <= size_classic or min(lns[1]) <= size_classic:
        return classic(first_matrix, second_matrix, pointers, ends)

    mids_i = [pointers[0][0] + lns[0][0] // 2, pointers[1][0] + lns[1][0] // 2]  # middles lines
    mids_j = [pointers[0][1] + lns[0][1] // 2, pointers[1][1] + lns[1][1] // 2]  # middles column

    # coords little matrix
    A = [pointers[0], (mids_i[0], mids_j[0])]
    B = [(pointers[0][0], mids_j[0]), (mids_i[0], ends[0][1])]
    C = [(mids_i[0], pointers[0][1]), (ends[0][0], mids_j[0])]
    D = [(mids_i[0], mids_j[0]), ends[0]]

    E = [pointers[1], (mids_i[1], mids_j[1])]
    F = [(pointers[1][0], mids_j[1]), (mids_i[1], ends[1][1])]
    G = [(mids_i[1], pointers[1][1]), (ends[1][0], mids_j[1])]
    H = [(mids_i[1], mids_j[1]), ends[1]]

    P1 = Strassen(first_matrix=first_matrix,                                 # A
                  second_matrix=addition_matrix2(first_matrix=second_matrix,  # (F - H) matrix
                                                second_matrix=second_matrix,
                                                pointers=[F[0], H[0]],
                                                ends=[F[1], H[1]],
                                                sign=-1),
                  pointers=[A[0], (0, 0)],
                  ends=[
                            A[1], (max(F[1][0] - F[0][0], H[1][0] - H[0][0]), max(F[1][1] - F[0][1], H[1][1] - H[0][1]))
                       ]
                  )

    P2 = Strassen(first_matrix=addition_matrix2(first_matrix=first_matrix,  # (A + B) matrix
                                               second_matrix=first_matrix,
                                               pointers=[A[0], B[0]],
                                               ends=[A[1], B[1]]),
                  second_matrix=second_matrix,                             # H
                  pointers=[(0, 0), H[0]],
                  ends=[
                        (max(A[1][0] - A[0][0], B[1][0] - B[0][0]), max(A[1][1] - A[0][1], B[1][1] - B[0][1])), H[1]
                       ]
                  )

    P3 = Strassen(first_matrix=addition_matrix2(first_matrix=first_matrix,  # (C + D) matrix
                                               second_matrix=first_matrix,
                                               pointers=[C[0], D[0]],
                                               ends=[C[1], D[1]]),
                  second_matrix=second_matrix,                             # E
                  pointers=[(0, 0), E[0]],
                  ends=[
                        (max(C[1][0] - C[0][0], D[1][0] - D[0][0]), max(C[1][1] - C[0][1], D[1][1] - D[0][1])), E[1]
                       ]
                  )

    P4 = Strassen(first_matrix=first_matrix,                                 # D
                  second_matrix=addition_matrix2(first_matrix=second_matrix,  # (G - E) matrix
                                                second_matrix=second_matrix,
                                                pointers=[G[0], E[0]],
                                                ends=[G[1], E[1]],
                                                sign=-1),
                  pointers=[D[0], (0, 0)],
                  ends=[
                        D[1], (max(E[1][0] - E[0][0], G[1][0] - G[0][0]), max(E[1][1] - E[0][1], G[1][1] - G[0][1]))
                       ]
                  )

    P5 = Strassen(first_matrix=addition_matrix2(first_matrix=first_matrix,  # (A + D) matrix
                                               second_matrix=first_matrix,
                                               pointers=[A[0], D[0]],
                                               ends=[A[1], D[1]]),
                  second_matrix=addition_matrix2(first_matrix=second_matrix,  # (E + H) matrix
                                                second_matrix=second_matrix,
                                                pointers=[E[0], H[0]],
                                                ends=[E[1], H[1]]),
                  )

    P6 = Strassen(first_matrix=addition_matrix2(first_matrix=first_matrix,  # (B - D) matrix
                                               second_matrix=first_matrix,
                                               pointers=[B[0], D[0]],
                                               ends=[B[1], D[1]],
                                               sign=-1),
                  second_matrix=addition_matrix2(first_matrix=second_matrix,  # (G + H) matrix
                                                second_matrix=second_matrix,
                                                pointers=[G[0], H[0]],
                                                ends=[G[1], H[1]]),
                  )

    P7 = Strassen(first_matrix=addition_matrix2(first_matrix=first_matrix,  # (A - C) matrix
                                               second_matrix=first_matrix,
                                               pointers=[A[0], C[0]],
                                               ends=[A[1], C[1]],
                                               sign=-1),
                  second_matrix=addition_matrix2(first_matrix=second_matrix,  # (E + F) matrix
                                                second_matrix=second_matrix,
                                                pointers=[E[0], F[0]],
                                                ends=[E[1], F[1]])
                  )

    Q1 = addition_matrix2(first_matrix=addition_matrix2(first_matrix=P5, second_matrix=P4),
                         second_matrix=addition_matrix2(first_matrix=P2, second_matrix=P6, sign=-1),
                         sign=-1)

    Q2 = addition_matrix2(first_matrix=P1, second_matrix=P2)
    Q3 = addition_matrix2(first_matrix=P3, second_matrix=P4)
    Q4 = addition_matrix2(first_matrix=addition_matrix2(first_matrix=P1, second_matrix=P5),
                         second_matrix=addition_matrix2(first_matrix=P3, second_matrix=P7),
                         sign=-1)

    a, b = lns[0][0] // 2, (lns[0][0] + 1) // 2
    massive = [[Q1, a], [Q2, a], [Q3, b], [Q4, b]]
    # print(f"AAAAAAA{a = }, {b = }, {pointers = }, {ends = }")
    # print(f"{first_matrix = }\n{second_matrix = }\n{Q1 = }\n{Q2 = }\n{Q3 = }\n{Q4 = }")

    for obj, size in massive:
        while len(obj) > size:
            obj.pop()

    for i in range(a):
        Q1[i][a:] = Q2[i][:b]
    for i in range(b):
        Q3[i][a:] = Q4[i][:b]
    Q1 += Q3

    # print(f"{Q1 = }")
    return Q1


def start_Strassen(first_matrix: T, second_matrix: T) -> T:
    n = len(first_matrix)
    k = degree2app(first_matrix) - n
    if k:
        temp = [0] * k
        for i in range(n):
            first_matrix[i] += temp
            second_matrix[i] += temp

        temp += [0] * n
        new_temp = [temp] * k
        first_matrix += new_temp
        second_matrix += new_temp

    result = Strassen(first_matrix, second_matrix)
    for i in range(k):
        result.pop()
    for i in range(n):
        result[i][n:] = []

    return result


def degree2app(matrix: T):
    ost, res, ln = 0, 1, len(matrix)
    while ln > 1:
        res *= 2
        ost = max(ost, ln % 2)
        ln //= 2

    return max(ost * 2 * res, len(matrix))


# =================================== !!! COPY PASTE FROM task_09 FROM Tasks-Python !!! ================================
F = list | tuple


def my_center(st, size: int):
    return f"{st}".center(size)


def my_print(*args):
    print("", *args, "", sep='|')


def format_table(benchmarks: F, algos: F, results: F):
    # sizes
    sizes = []
    header_size = len(max('Benchmark', *benchmarks, key=len)) + 2
    for ind in range(len(algos)):
        column = [len(str(elem[ind])) for elem in results]
        sizes.append(max(len(algos[ind]), max(column)) + 2)

    # Header
    my_print(my_center("Benchmark", header_size), *[my_center(algos[ind], sizes[ind]) for ind in range(len(algos))])
    my_print("-" * (sum(sizes) + header_size + len(algos)))

    # Body
    for ind in range(len(benchmarks)):
        my_print(my_center(benchmarks[ind], header_size), *[my_center(e, sizes[j]) for j, e in enumerate(results[ind])])
# ======================================================================================================================


gg_start = 0
gg_end = 0
if __name__ == "__main__":
    debug = False
    if debug:
        rty = [[1, 2, 3, 4, 5],
               [1, 2, 3, 4, 5],
               [1, 2, 3, 4, 5],
               [1, 2, 3, 4, 5],
               [1, 2, 3, 4, 5]]
        tt = addition_matrix2(first_matrix=rty,
                             second_matrix=rty,
                             pointers=[(0, 2), (2, 2)],
                             ends=[(2, 5), (2, 5)],
                             sign=-1)
        print(tt)
    else:
        # base_test()
        # test1()

        gg_start = time.time()
        stand()
        print(f"\nAll time: {gg_end - gg_start}\n")

        # zxc = time.time()
        # q1, q2 = generate_test(312)
        # print(time.time() - zxc)
        # print('AAAAAAA')
        # zxc = time.time()
        # Strassen(q1, q2)
        # print(time.time() - zxc)

        # t = 4
        # qwe = [generate_test(16 << t), generate_test(32 << t)]
        # funcs = [classic, recursive, Strassen]
        # for one, two in qwe:
        #     print('\n====================================================================================\n')
        #     for func in funcs:
        #         times_func = exec_time_algo(one, two, algo=func)
        #         asd = ["\t".join([format(x, '.6f') for x in times_func])]
        #         print(*asd, func.__name__, sep='\t')

"""
Слишком много копипаста! надо будет пофиксить!!!
"""
