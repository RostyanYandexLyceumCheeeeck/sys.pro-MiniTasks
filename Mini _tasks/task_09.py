T = list | tuple


def my_center(st, size: int):
    return f"{st}".center(size)


def my_print(*args):
    print("", *args, "", sep='|')


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


if __name__ == "__main__":
    format_table(["best case", "worst case"],
                 ["quick sort", "merge sort", "bubble sort"],
                 [[1.23, 1.56, 2.0], [3.3, 2.9, 3.9]])
