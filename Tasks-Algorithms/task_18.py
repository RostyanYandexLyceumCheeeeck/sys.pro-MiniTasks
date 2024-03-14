from copy import copy


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


oper = {
    # operator: (precedence, left associativity, function)
    "**": (-0, True, lambda x, y: [x ** y]),
    "!": (-1, False, lambda x, y: [x, not y]),
    "~": (-1, False, lambda x, y: [x, ~y]),
    "*": (-2, True, lambda x, y: [x * y]),
    "/": (-2, True, lambda x, y: [x / y]),
    "%": (-2, True, lambda x, y: [x % y]),
    "+": (-3, True, lambda x, y: [x + y]),
    "-": (-3, True, lambda x, y: [x - y]),
    "<<": (-4, True, lambda x, y: [x << y]),
    ">>": (-4, True, lambda x, y: [x >> y]),
    "&": (-5, True, lambda x, y: [x & y]),
    "^": (-6, True, lambda x, y: [x ^ y]),
    "|": (-7, True, lambda x, y: [x | y]),
    "&&": (-8, True, lambda x, y: [x and y]),
    "||": (-9, True, lambda x, y: [x or y]),

}
matching_brackets = {
    '(': ')',
    '[': ']',
    '{': '}',
}


def string_to_rpn(arr: str, start: int = 0, bracket: str = '', result: list[str] = []) -> str | int:
    stack = Stack()
    i = start
    while i < len(arr):
        elem = arr[i]
        if elem == ' ':
            i += 1
            continue

        if elem not in oper:
            if elem in matching_brackets:
                i = string_to_rpn(arr, i + 1, elem, result)
                continue

            if elem in "]})":
                if bracket:
                    if matching_brackets[bracket] == elem:
                        break
                    raise ValueError
                i += 1
                continue
            result.append(elem)

        else:
            while not stack.empty():
                last = oper[stack.peek()]
                curr = oper[elem]
                if not ((last[0] > curr[0]) or (last[0] == curr[0] and curr[1])):
                    break
                result.append(stack.pop())
            stack.push(elem)
        i += 1

    while not stack.empty():
        result.append(stack.pop())

    return i if bracket else " ".join(result)


def rpn_to_int(arr: str):
    arr = arr.split()
    stack = Stack()
    for elem in arr:
        if elem not in oper:
            stack.push(elem)
        elif not stack.empty():
            b = stack.pop()
            a = stack.pop()
            for res in oper[elem][2](int(a), int(b)):
                stack.push(res)
    return stack.pop()


def get_test(number: int = -1):
    tests = {
        0: "1 - 5 * 3",
        1: "1 - 5 ^ 3 * 2",
        2: "4 - (1 - 2)",
        3: "(1 - 2) - 4",
        4: "9 + (1 - 2 - (8 - (4 + 3)))",
        5: "9 + (1 - 2 * (8 - (4 + 3)))",
    }
    return tests[number]


def empty(*args, **kwargs):
    return


def title_factory(objs, length):
    res = []
    for name, sep, value, end in objs:
        res.append(f"{name}{sep}{value}{end}")
    res = "".join(res).center(length, '=')
    return res


def test_factory(start: int = 0, number_test: int = -1):
    title = {'values': [title_factory([("TEST", ' ', number_test, '')], 30),
                        title_factory([(' start', '=', start, ' ')], 30)],
             'end': '\n'} if number_test > -1 else {'values': '', 'end': ''}
    func = print if debug else empty

    arr = get_test(number_test)
    c_arr = copy(arr)

    func(*title['values'], sep='\n', end=title['end'])
    func(arr)
    arr = string_to_rpn(arr, start, result=list())
    func(arr)

    res_true = eval(c_arr)
    my_res = rpn_to_int(arr)
    func(res_true, my_res)
    func()
    assert res_true == my_res


def base_test():
    for i in range(6):
        test_factory(0, i)


if __name__ == "__main__":
    debug = True
    base_test()

"""
1 - 5 * 3  ==> 1 5 3 * - ==> -14 ==>
==== 1 5 3 * - ====
==== 1 15 - ====
==== -14 ====

1 - 5 ^ 3 * 2 ==> 1 5 - 3 2 * ^ ==> -6 ==> 
==== 1 5 - 3 2 * ^ ====
==== -4 3 2 * ^ ====
==== -4 6 ^ ====
==== -6 ====

4 - (1 - 2)  ==> 4 1 2 - - ==> 5 ==> 
==== 4 1 2 - - ====
==== 4 -1 - ====
==== 5 ====

(1 - 2) - 4  ==> 1 2 - 4 - ==> -5
==== 1 2 - 4 - ====
==== -1 4 - ====
==== -5 ====

9 + (1 - 2 - (8 - (4 + 3))) ==> 9 1 2 - 8 4 3 + - - + ==> 7 ==> 
==== 9 1 2 - 8 4 3 + - - + ====
==== 9 -1 8 4 3 + - - + ====
==== 9 -1 8 7 - - + ====
==== 9 -1 1 - + ====
==== 9 -2 + ====
==== 7 ====


9 + (1 - 2 * (8 - (4 + 3))) ==> 9 1 2 8 4 3 + - * - + ==> 7 ==> 
==== 9 1 2 8 4 3 + - * - + ====
==== 9 1 2 8 7 - * - + ====
==== 9 1 2 1 * - + ====
==== 9 1 2 - + ====
==== 9 -1 + ====
==== 8 ====
"""