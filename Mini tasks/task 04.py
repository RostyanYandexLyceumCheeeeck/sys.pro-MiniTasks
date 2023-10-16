first = {
    ('SSS+', '1000 - 7'): 22332,
    'one_key': 22332,
    'two_key': (1, 'a', 33.0),
    111: 'asd',
    'qqqqq': 22332,
    'aass': 22332,
    ('123', 'zxc'): 22332,
    ('qwe', '222'): 22332,
    }
second: dict = {}

for key, value in first.items():
    try:
        second[value] = (*second[value], key) if isinstance(second[value], tuple) else (second[value], key)
    except KeyError:
        second[value] = (key, ) if isinstance(key, tuple) else key

print(second)