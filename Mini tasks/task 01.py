x = int(input())
count = 0

if x < 0:
    x = abs(x)
    flag = True

    while x:
        if x % 2:
            flag = False
        elif not flag:
            count += 1
        x >>= 1

    count += 2
else:
    while x:
        count += x % 2
        x >>= 1

print(count)
