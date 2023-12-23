def chain(lst_iter: list | tuple):
    for elem in lst_iter:
        yield from elem


if __name__ == "__main__":
    asd = chain([iter([1, 2, 3]), iter(["a", 'zxczcc', None, False]), iter(range(4, 12))])
    for a in asd:
        print(a)
