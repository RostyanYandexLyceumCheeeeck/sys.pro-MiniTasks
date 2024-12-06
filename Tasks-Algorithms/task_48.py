from math import inf
from time import time
from random import randint
from itertools import permutations, combinations


T = list | tuple
# FILE = "task_48_stand.txt"
FILE = None


def generate_graph(n: int):
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            graph[i][j] = graph[j][i] = randint(1, 8)
    return graph


def bruteforce(graph):
    path = inf
    n = len(graph)

    for variant in permutations(range(1, n)):
        path = min(path, 
                   graph[0][variant[0]] + sum(graph[variant[i]][variant[i+1]]
                                              for i in range(len(variant) - 1)
                                              ) + graph[variant[-1]][0]
                   )
    return path


def bellman_held_karp(graph):
    n = len(graph)
    m = 1 << n
    matrix = [[inf] * m for _ in range(n)]
    matrix[0][1] = 0

    for size_set in range(1, n):
        for subset in combinations(range(1, n), size_set):
            bit_subset = sum(1 << i for i in subset) + 1
            subset = [0, *subset]
            for last_v in subset:
                bit_last_subset = bit_subset ^ (1 << last_v)
                matrix[last_v][bit_subset] = min(matrix[before_last][bit_last_subset] + graph[before_last][last_v]
                                                 for before_last in subset if before_last != last_v)

    bit_all_subset = (1 << n) - 1
    return min(matrix[last_v][bit_all_subset] + graph[0][last_v] for last_v in range(1, n))


def collect_statistic():
    bench = []
    algos = ['Bruteforce', "Bellman-Held_karp"]
    times = []
    support_collect_statistic(2, 14, bench, algos, times)
    # support_collect_statistic(14, 15, bench, algos, times)
    format_table(bench, algos, times)


def support_collect_statistic(min_size, max_size, bench, algos, times):
    reform_func = lambda x: f"0{x}" if x < 10 else str(x)

    for n in range(min_size, max_size):
        bench.append(f"full graph: {reform_func(n)}x{reform_func(n)}")
        graph = generate_graph(n)
        local_times = []
        for func in (bruteforce, bellman_held_karp):
            start = time()
            func(graph)
            local_times.append(round(time() - start, 6))
        times.append(local_times)


def my_center(st, size: int):
    return f"{st}".center(size)


def my_print(*args):
    if not FILE:
        print("", *args, "", sep='|')
        return
    with open(FILE, 'a', encoding='utf-8') as f:
        print("", *args, "", sep='|', file=f)


def format_table(benchmarks: T, algos: T, results: T):
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


def test():
    for n in range(2, 7):
        for _ in range(3):
            graph = generate_graph(n)
            assert bruteforce(graph) == bellman_held_karp(graph)


if __name__ == "__main__":
    test()
    collect_statistic()
