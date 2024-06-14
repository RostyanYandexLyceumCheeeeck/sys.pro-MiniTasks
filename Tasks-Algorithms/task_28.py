from random import randint, random
from math import log, log2

MAX_VALUE = int(random() * 10**randint(6, 20))
MIN_VALUE = -int(random() * 10**randint(6, 20))


def isPrime(x: int):
    sqr = int(x**0.5) + 1
    for i in range(2, sqr):
        if not x % i:
            return False
    return True


def nextPrime(n: int):
    while not isPrime(n):
        n += 1 + n % 2
    return n


class FilterBlumIP:
    class HashIP:
        def __init__(self):
            self.keys = [randint(MIN_VALUE, MAX_VALUE) for _ in range(4)]

        def hashing(self, ip: list[int]):
            return sum(ip[i] * self.keys[i] for i in range(len(self.keys)))

    def __init__(self, err, count):
        k = -log2(err)
        n = int(k / log(2) * count) + 1
        n = nextPrime(n)
        print(f"{n = }")
        self.funcs = [FilterBlumIP.HashIP() for _ in range(int(k) + 1)]
        self.bits = [0 for _ in range(n)]

    def insert(self, key: str | list[int]):
        if isinstance(key, str):
            key = list(map(int, key.split('.')))

        for func in self.funcs:
            self.bits[func.hashing(key) % len(self.bits)] = 1

    def lookup(self, key: str | list[int]):
        if isinstance(key, str):
            key = list(map(int, key.split('.')))

        return all(self.bits[func.hashing(key) % len(self.bits)] for func in self.funcs)


if __name__ == "__main__":
    degree = 16
    er, co = 0.0001, 1 << degree
    Fil = FilterBlumIP(er, co)

    dataset = [[z, w, y, x]  # f"{z}.{w}.{y}.{x}"
               for x in range(1 << (degree//4))
               for y in range(1 << (degree//4))
               for w in range(1 << (degree//4))
               for z in range(1 << (degree//4))]

    new_co = 0
    for elem in dataset:
        new_co += int(Fil.lookup(elem))
        Fil.insert(elem)

    new_er = new_co / len(dataset)

    print("count =", len(dataset))
    print("error =", er, "\tcount =", co)
    print(f"n_err = {format(new_er, '.3f')}", f"\tcount_err = {new_co}")
