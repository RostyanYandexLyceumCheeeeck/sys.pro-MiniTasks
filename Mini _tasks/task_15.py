import matplotlib.animation as animation
import matplotlib.pyplot as plt
from random import randint
from pprint import pp
import numpy as np
import time
import copy

SIZE = 1024
GENERATIONS = 128
history = []
ind = 0


def execution_time(func):
    def posrednik(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print(f"{func.__name__} is time {time.time() - start} seconds.")
    return posrednik


def generator_field():
    res = []
    for i in range(SIZE):
        lst = []
        for j in range(SIZE):
            lst.append(randint(0, 1))
        res.append(lst)
    return res


def realization_Python(lst: list):
    copy_lst = copy.deepcopy(lst)
    for i in range(SIZE):
        for j in range(SIZE):
            neighbours = sum([copy_lst[line % SIZE][column % SIZE] if line != i or column != j else False
                             for line in [i - 1, i, i + 1] for column in [j - 1, j, j + 1]])
            if neighbours == 3:
                lst[i][j] = 1
            else:
                lst[i][j] = min(int(neighbours == 2), lst[i][j])


@execution_time
def start_Python(lst: list):
    for _ in range(GENERATIONS):
        realization_Python(lst)


def realization_Numpy(lst):
    arr = np.array(lst)
    for i in range(SIZE):
        for j in range(SIZE):
            neighbours = sum([arr[line % SIZE][column % SIZE] if line != i or column != j else False
                              for line in [i - 1, i, i + 1] for column in [j - 1, j, j + 1]])
            if neighbours == 3:
                lst[i][j] = 1
            else:
                lst[i][j] = min(int(neighbours == 2), lst[i][j])


@execution_time
def start_Numpy(lst):
    for _ in range(GENERATIONS):
        realization_Numpy(lst)


def create_history(lst):
    for _ in range(GENERATIONS):
        history.append(copy.deepcopy(lst))
        realization_Python(lst)
    history.append(lst)


def animate(frame):
    global ind
    plt.imshow(history[ind])
    ind += 1
    if ind == GENERATIONS + 1:
        exit(0)


if __name__ == "__main__":
    test = generator_field()
    start_Python(copy.deepcopy(test))
    start_Numpy(np.array(copy.deepcopy(test)))

    # animation
    create_history(test)
    fig = plt.figure()
    anim = animation.FuncAnimation(fig, animate, frames=GENERATIONS, interval=0)
    plt.show()
