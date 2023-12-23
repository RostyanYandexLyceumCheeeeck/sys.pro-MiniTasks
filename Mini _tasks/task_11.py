import sys


def singleton(mcls):
    slov = {}
    count_ref = {}

    class Intermediary(mcls):
        def __new__(cls, *args, **kwargs):
            if mcls not in slov or sys.getrefcount(slov[mcls]) == count_ref[mcls]:
                slov[mcls] = mcls(*args, **kwargs)
                count_ref[mcls] = sys.getrefcount(slov[mcls])
            return slov[mcls]
    return Intermediary


@singleton
class Foo:
    test = 123

    def __init__(self):
        print('new Foo')


@singleton
class Bar:
    def __init__(self):
        print('new Bar')


if __name__ == "__main__":
    # Test 1
    print("======Test 1======")
    a = Foo()
    print(Foo.test)
    a1 = Foo()
    a2 = Foo()
    print(id(a) == id(a1) == id(a2))  # True

    # Test 2
    print("\n======Test 2======")
    b = Bar()
    save_id_b = id(b)
    del b
    b = Bar()
    print(save_id_b == id(b))  # False

    # Test 3
    print("\n======Test 3======")
    del a
    del a1
    a = Foo()
    print(id(a) == id(a2))  # True

    # Test 4
    print("\n======Test 4======")
    save_id_a = id(a)
    del a
    del a2
    a = Foo()
    print(save_id_a == id(a))  # False
