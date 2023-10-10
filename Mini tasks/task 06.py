def flatten(start: list, finish: None | list = None) -> list:
    """
    хвостовая рекурсия для распаковки всех листов, вложенных в начальный лист.

    :param start: входной массив.
    :param finish: выходной массив. По умолчанию создаётся новый.
    :return: возвращает лист со всеми элементами и элементами распакованных массивов.

    Пример:
        >>> flatten([1, 2, [4, 5], [6, [7]], 8])
        [1, 2, 4, 5, 6, 7, 8]
    """
    if not finish:
        finish = []
    for elem in start:
        flatten(elem, finish) if isinstance(elem, list) else finish.append(elem)
    return finish


print(flatten([1, 2, [3, [4, [5, 6, 7]]]]))
