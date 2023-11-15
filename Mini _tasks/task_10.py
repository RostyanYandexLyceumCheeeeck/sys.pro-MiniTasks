class LRUCache:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.cache = {}

    def put(self, key, value):
        if self.get(key) is None and len(self.cache) == self.capacity and key not in self.cache:
            del self.cache[self.cache.__iter__().__next__()]
        self.cache[key] = value

    def get(self, key):
        try:
            res = self.cache[key]
            del self.cache[key]
            self.cache[key] = res
            return res
        except KeyError:
            return None


if __name__ == "__main__":
    cache = LRUCache()
    for i in range(16):
        cache.put(i, i)
    print(f"cache: {cache.cache}")
    cache.put(0, 160)
    cache.put(17, 17)
    print(f"cache: {cache.cache}")
