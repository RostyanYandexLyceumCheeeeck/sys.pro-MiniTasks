# https://leetcode.com/problems/maximum-frequency-stack/submissions/1236009886

class SimpleStack:
    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1] if self.stack else None


class FreqStack:
    def __init__(self):
        self.stack: dict = {}
        self.cache = {}
        self.count_max = 0

    def push(self, val: int) -> None:
        self.cache[val] = count = self.cache[val] + 1 if val in self.cache else 1
        if count not in self.stack:
            self.stack[count] = SimpleStack()

        self.stack[count].push(val)
        self.count_max = max(self.count_max, count)

    def pop(self) -> int:
        res = self.stack[self.count_max].pop()
        self.cache[res] -= 1

        if self.stack[self.count_max].peek() is None:
            self.count_max -= 1
        return res


def testing(arr, temp):
    qwe = FreqStack()
    for i in range(1, len(arr)):
        if arr[i] == 'push':
            qwe.push(temp[i][0])
        else:
            print(qwe.pop(), temp[i])


def base_test():
    freqStack = FreqStack()
    freqStack.push(5)  # Стек равен[5]
    freqStack.push(7)  # Стек равен[5, 7]
    freqStack.push(5)  # Стек равен[5, 7, 5]
    freqStack.push(7)  # Стек равен[5, 7, 5, 7]
    freqStack.push(4)  # Стек равен[5, 7, 5, 7, 4]
    freqStack.push(5)  # Стек равен[5, 7, 5, 7, 4, 5]
    print(freqStack.pop())  # 5
    print(freqStack.pop())  # 7
    print(freqStack.pop())  # 5
    print(freqStack.pop())  # 4
    print("========= END base_test =========\n")


if __name__ == "__main__":
    # base_test()
    arr = ["FreqStack", "push", "push", "push", "push", "push", "push", "pop", "push", "pop", "push", "pop", "push",
           "pop", "push", "pop", "pop", "pop", "pop", "pop", "pop"]
    zxc = [[], [4], [0], [9], [3], [4], [2], [], [6], [], [1], [], [1], [], [4], [], [], [], [], [], []]
    testing(arr, zxc)

