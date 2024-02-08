def swap_key_and_value(first: dict, second: dict = {}) -> dict:
    for key, value in first.items():
        try:
            second[value] = (*second[value], key) if isinstance(second[value], tuple) else (second[value], key)
        except KeyError:
            second[value] = (key, ) if isinstance(key, tuple) else key
    return second


if __name__ == "__main__":
    one = {
        ('SSS+', '1000 - 7'): 22332,
        'one_key': 22332,
        'two_key': (1, 'a', 33.0),
        111: 'asd',
        'qqqqq': 22332,
        'aass': 22332,
        ('123', 'zxc'): 22332,
        ('qwe', '222'): 22332,
        }

    two: dict = swap_key_and_value(one)
    three = {}
    swap_key_and_value(one, three)

    print(two)
    print(three)