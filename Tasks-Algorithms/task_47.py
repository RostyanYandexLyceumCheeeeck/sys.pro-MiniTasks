from copy import copy


class Stack:
    def __init__(self, value=None, nxt=None):
        self.value = value
        self.nxt = nxt

    def push(self, val):
        return Stack(val, self)

    def top(self):
        if self.empty():
            raise IndexError("Stack is empty!")
        return self.value

    def pop(self):
        self.top()
        return self.nxt
    
    def empty(self):
        return self.value is None


class Queue:
    def __init__(self, size=0, help2_size=-1, master=Stack(), help=Stack(), master2=Stack(), help2=Stack()):
        self.size = size
        self.help2_size = help2_size

        self.help = help
        self.help2 = help2
        self.master = master
        self.master2 = master2

    def fixed(self):
        if self.help2_size == -1:
            self.help2_size = self.size
            self.help2 = Stack(None, None)
            self.master2 = self.master

        if self.help2_size > 0:
            self.help2_size -= 1
            self.help2 = self.help2.push(self.master2.top())
            self.master2 = self.master2.pop()

        if self.help2_size == 0:
            self.help = self.help2
            self.help2_size = -1
            self.help2 = self.master2 = Stack(None, None)
        return copy(self)

    def push(self, val):
        return Queue(self.size + 1, self.help2_size, self.master.push(val), self.help, self.master2, self.help2).fixed()

    def top(self):
        return self.help.top()

    def pop(self):
        if self.empty():
            raise IndexError("Queue is empty!")
        return Queue(self.size - 1, max(-1, self.help2_size - 1),
                     self.master, self.help.pop(), self.master2, self.help2).fixed()

    def empty(self):
        return not bool(self.size)

    def __copy__(self):
        return Queue(self.size, self.help2_size, self.master, self.help, self.master2, self.help2)


class PersistentQueue:
    def __init__(self):
        self.versions: list[Queue] = [Queue()]

    def push(self, timestamp: int, val):
        self.versions.append(self.versions[timestamp].push(val))
        return len(self.versions)

    def pop(self, timestamp: int):
        self.versions.append(self.versions[timestamp].pop())
        return len(self.versions), self.versions[timestamp].top()

    def get(self, timestamp: int):
        return self.versions[timestamp]

    def empty(self):
        return bool(self.versions)


def test_1():
    pq = PersistentQueue()  # [ ,]
    pq.push(0, 1)  # [ , 1]
    pq.push(1, 3)  # [ , 1, 1->3]
    pq.push(2, 4)  # [ , 1, 1->3, 1->3->4]
    pq.push(3, 1)  # [ , 1, 1->3, 1->3->4, 1->3->4->1]
    pq.push(0, 7)  # [ , 1, 1->3, 1->3->4, 1->3->4->1, 7]

    assert pq.pop(4)[1] == 1   # [ , 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1]
    assert pq.pop(3)[1] == 1   # [ , 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4]
    assert pq.pop(7)[1] == 3   # [ , 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4]

    assert pq.pop(4)[1] == 1   # [ , 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1]
    assert pq.pop(9)[1] == 3   # [ , 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1]
    assert pq.pop(10)[1] == 4  # [ , 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1]
    assert pq.pop(11)[1] == 1  # [ , 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1,  ,]

    assert pq.pop(4)[1] == 1
    # [ , 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1,  , 3->4->1]
    assert pq.pop(4)[1] == 1
    # [ , 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1,  , 3->4->1, 3->4->1]
    assert pq.pop(4)[1] == 1
    # [ , 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1,  , 3->4->1, 3->4->1, 3->4->1]
    assert pq.pop(4)[1] == 1
    # [ , 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1,  , 3->4->1, 3->4->1, 3->4->1, 3->4->1]


if __name__ == "__main__":
    test_1()
