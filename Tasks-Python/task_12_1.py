def cycle(obj):
    while True:
        yield from obj


if __name__ == "__main__":
    asd = cycle(iter([1, 2, 3]))
    for _ in range(11):
        print(next(asd))
