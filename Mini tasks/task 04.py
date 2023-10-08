first = {'one_key': 22332,
         'two_key': (1, 'a', 33.0),
         111: 'asd',
         'qqqqq': 22332}
second: dict = {}

for key, value in first.items():
    try:
        second[value].append(key)
    except KeyError:
        second[value] = key
    except AttributeError:
        second[value] = [second[value], key]

for key, value in second.items():
    second[key] = (*second[key], ) if isinstance(second[key], list) else second[key]

print(second)