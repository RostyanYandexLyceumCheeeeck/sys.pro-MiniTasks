import sys


def singleton(cls):
    slov = {}
    count_ref = {}

    def posrednik(*args, **kwargs):
        if cls not in slov or sys.getrefcount(slov[cls]) == count_ref[cls]:
            slov[cls] = cls(*args, **kwargs)
            count_ref[cls] = sys.getrefcount(slov[cls])
        return slov[cls]
    return posrednik


@singleton
class Foo:
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
    a1 = Foo()
    a2 = Foo()
    print(id(a) == id(a1) == id(a2))

    # Test 2
    print("\n======Test 2======")
    b = Bar()
    save_id_b = id(b)
    del b
    b = Bar()
    print(save_id_b == id(b))

    # Test 3
    print("\n======Test 3======")
    del a
    del a1
    a = Foo()
    print(id(a) == id(a2))

    # Test 4
    print("\n======Test 4======")
    save_id_a = id(a)
    del a
    del a2
    a = Foo()
    print(save_id_a == id(a))