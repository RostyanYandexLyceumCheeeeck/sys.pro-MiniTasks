T = list | tuple


def my_ljust(st, size: int):
    return f" {st}".ljust(size)


def format_table(benchmarks: T, algos: T, results: T):
    res_str = [str(elem) for res in results for elem in res]
    size = len(f"{max('Benchmark', *benchmarks, *algos, *res_str, key=len)}") + 2

    # Header
    print("", my_ljust("Benchmark", size), *[my_ljust(algo, size) for algo in algos], "", sep='|')
    print("|", "-" * (size * (len(algos) + 1) + len(algos)), "|", sep='')

    # Body
    for i_bench in range(len(benchmarks)):
        print("", my_ljust(benchmarks[i_bench], size), *[my_ljust(el, size) for el in results[i_bench]], "", sep='|')


if __name__ == "__main__":
    format_table(["best case", "worst case"],
                 ["quick sort", "merge sort", "bubble sort"],
                 [[1.23, 1.56, 2.0], [3.3, 2.9, 3.9]])
