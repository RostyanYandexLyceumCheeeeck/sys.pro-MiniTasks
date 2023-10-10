def flatten(start: list, finish: None | list = None, depth: int | None = None) -> list:
    """
    хвостовая рекурсия для распаковки всех листов, вложенных в начальный лист.

    :param start: входной массив.
    :param finish: выходной массив. По умолчанию - создаётся пустой.
    :param depth: макс.глубина распаковки. По умолчанию - распоковывает всё.
    :return: возвращает лист со всеми элементами и элементами распакованных массивов.

    Пример:
        >>> flatten([1, 2, [4, 5], [6, [7, [8]]], 9])
        [1, 2, 4, 5, 6, 7, 8, 9]
        >>> flatten([1, 2, [4, 5], [6, [7, [8]]], 9], depth=1)
        [1, 2, 4, 5, 6, [7, [8]], 9]
    """
    if not finish:
        finish = []

    for elem in start:
        if depth == 0 or not isinstance(elem, list):
            finish.append(elem)
        else:
            flatten(elem, finish, depth - 1) if depth else flatten(elem, finish)

    return finish


print(flatten([1, 2, [4, 5], [6, [7, [8]]], 9], depth=2))
