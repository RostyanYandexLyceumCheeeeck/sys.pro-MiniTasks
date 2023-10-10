def foo(one, two):
    """test function."""
    return one ** two


def baz(one, two, three=777):
    """test function."""
    return one // two * three


def specialize(func, *args, **kwargs):
    """
    :param func: Применяемая функция.
    :param args: Позиционные аргументы.
    :param kwargs: Именованные аргументы.
    :return: Возвращает функцию, использующую func.

    Пример:
        def sum(x, y):
            return x + y
        >>> x = specialize(sum, y=7)
        >>> print(x(10))
        17
    """
    def posrednik(*first_args, **first_kwargs):
        return func(*first_args, *args, **first_kwargs, **kwargs)
    return posrednik


x = specialize(foo, two=7)
y = specialize(foo, 10, 2)
w = specialize(baz, 20, three=79)
z = specialize(baz, two=79, three=7770)

print(x(10))
print(y())
print(w(30))
print(z(30))


