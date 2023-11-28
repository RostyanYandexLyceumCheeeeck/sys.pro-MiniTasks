def chain(lst_obj: list | tuple):
    class IteratorToIterators:
        def __init__(self, its):
            self._iterators = its
            self._ptr = 0

        def __iter__(self):
            return self

        def __next__(self):
            try:
                return next(self._iterators[self._ptr])
            except StopIteration:
                self._ptr += 1
                if self._ptr == len(self._iterators):
                    raise StopIteration
                return next(self._iterators[self._ptr])

    return IteratorToIterators(lst_obj)


if __name__ == "__main__":
    asd = chain([iter([1, 2, 3]), iter(["a", 'zxczcc', None, False]), iter(range(4, 12))])
    for a in asd:
        print(a)
