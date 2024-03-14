# https://leetcode.com/problems/min-stack/submissions/1203817675
class Stack:
    def __init__(self):
        self.data = []

    def pop(self):
        return self.data.pop()

    def push(self, value):
        self.data.append(value)

    def peek(self):
        return self.data[-1]

    def empty(self) -> bool:
        return not bool(len(self.data))


class MinStack(Stack):
    def __init__(self):
        super().__init__()
        self.min_data = Stack()

    def pop(self):
        res = self.data.pop()
        if not self.min_data.empty() and res == self.min_data.peek():
            self.min_data.pop()
        return res

    def push(self, value):
        self.data.append(value)
        if self.min_data.empty() or value <= self.min_data.peek():
            self.min_data.push(value)

    def get_min(self):
        return self.min_data.peek() if not self.min_data.empty() else None


if __name__ == "__main__":
    minStack = MinStack()
    minStack.push(-2)
    minStack.push(0)
    minStack.push(-3)
    print(minStack.get_min())  # return -3
    minStack.pop()
    print(minStack.peek())  # return 0
    print(minStack.get_min())  # return -2
