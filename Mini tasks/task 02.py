from random import randint

first = [randint(-1000, 1000) for _ in range(randint(0, 15))]
second = [chr(randint(32, 126)) for _ in range(randint(0, 15))]
result = []

for i in range(min(len(first), len(second))):
    result.append((first[i], second[i]))

print(f'{first =  }')
print(f'{second = }')
print(f'{result = }')