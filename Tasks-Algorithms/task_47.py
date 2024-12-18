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

    def __str__(self):
        return f"Stack <{self.value}, {self.nxt}>"


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
    pq.push(0, 1)  # [_, 1]
    pq.push(1, 3)  # [_, 1, 1->3]
    pq.push(2, 4)  # [_, 1, 1->3, 1->3->4]
    pq.push(3, 1)  # [_, 1, 1->3, 1->3->4, 1->3->4->1]
    pq.push(0, 7)  # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7]
    # count: 5

    assert pq.pop(4)[1] == 1   # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1]
    assert pq.pop(3)[1] == 1   # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4]
    assert pq.pop(7)[1] == 3   # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4]
    # count: 8

    assert pq.pop(4)[1] == 1   # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1]
    assert pq.pop(9)[1] == 3   # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1]
    assert pq.pop(10)[1] == 4  # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1]
    assert pq.pop(11)[1] == 1  # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _]
    # count: 12

    assert pq.pop(4)[1] == 1
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1]
    assert pq.pop(4)[1] == 1
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1]
    assert pq.pop(4)[1] == 1
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1]
    assert pq.pop(4)[1] == 1
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1]
    # count: 16

    assert pq.pop(5)[1] == 7
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _]
    assert pq.pop(2)[1] == 1
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3]
    assert pq.pop(18)[1] == 3
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _]
    # count: 19

    pq.push(19, 8)
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8]
    assert pq.pop(20)[1] == 8
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _]
    # count: 21

    pq.push(21, 9)
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9]
    pq.push(22, 11)
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11]
    pq.push(22, 10)
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10]
    # count: 24

    assert pq.pop(23)[1] == 9
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11]
    assert pq.pop(25)[1] == 11
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _]
    assert pq.pop(24)[1] == 9
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10]
    assert pq.pop(27)[1] == 10
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _]
    # count: 28

    assert pq.pop(23)[1] == 9
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11]
    assert pq.pop(25)[1] == 11
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _]
    assert pq.pop(24)[1] == 9
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10]
    assert pq.pop(27)[1] == 10
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _]
    # count: 32

    pq.push(32, 100)
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100]
    pq.push(33, 101)
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101]
    pq.push(34, 102)
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102]
    pq.push(35, 103)
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103]
    # count: 36

    assert pq.pop(33)[1] == 100
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _]
    assert pq.pop(34)[1] == 100
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101]
    assert pq.pop(35)[1] == 100
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102]
    assert pq.pop(36)[1] == 100
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103]
    # count: 40

    assert pq.pop(38)[1] == 101
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103, _]
    assert pq.pop(39)[1] == 101
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103, _, 102]
    assert pq.pop(40)[1] == 101
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103, _, 102, 102->103]
    # count: 43

    assert pq.pop(42)[1] == 102
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103, _, 102, 102->103, _]
    assert pq.pop(43)[1] == 102
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103, _, 102, 102->103, _, 103]
    # count: 45

    assert pq.pop(45)[1] == 103
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103, _, 102, 102->103, _, 103, _]
    # count: 46

    empties = [0, 12, 17, 19, 21, 26, 28, 30, 32, 37, 41, 44, 46]
    for i in empties:
        assert pq.versions[i].empty()

    others = filter(lambda x: x not in set(empties), range(47))
    for i in others:
        assert not pq.versions[i].empty()

    pq.push(46, 200)
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103, _, 102, 102->103, _, 103, _, 200]
    assert pq.pop(47)[1] == 200
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103, _, 102, 102->103, _, 103, _, 200, _]
    # count: 48

    pq.push(48, 201)
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103, _, 102, 102->103, _, 103, _, 200, 201]
    assert pq.pop(49)[1] == 201
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103, _, 102, 102->103, _, 103, _, 200, 201, _]
    # count: 50

    pq.push(50, 202)
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103, _, 102, 102->103, _, 103, _, 200, 201, _, 202]
    assert pq.pop(49)[1] == 201
    # [_, 1, 1->3, 1->3->4, 1->3->4->1, 7, 3->4->1, 3->4, 4, 3->4->1, 4->1, 1, _, 3->4->1, 3->4->1, 3->4->1, 3->4->1,
    #  _, 3, _, 8, _, 9, 9->11, 9->10, 11, _, 10, _, 11, _, 10, _, 100, 100->101, 100->101->102, 100->101->102->103,
    #  _, 101, 101->102, 101->102->103, _, 102, 102->103, _, 103, _, 200, 201, _, 202, _]
    # count: 52

    for i in range(47, 53, 2):
        assert not pq.versions[i].empty()
        assert pq.versions[i+1].empty()

    print()  # debut points


if __name__ == "__main__":
    test_1()
