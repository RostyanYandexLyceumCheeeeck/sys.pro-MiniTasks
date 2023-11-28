import copy


def cycle(obj):
    class Clone:
        def __init__(self, it):
            self._iterator = it
            self._copy = copy.copy(it)

        def __iter__(self):
            return self

        def __next__(self):
            try:
                return next(self._copy)
            except StopIteration:
                self._copy = copy.copy(self._iterator)
                return next(self._copy)

    return Clone(obj)


if __name__ == "__main__":
    asd = cycle(iter([1, 2, 3]))
    for _ in range(11):
        print(next(asd))
