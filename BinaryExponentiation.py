a = 1245899557745662123344557
e = 65537
n = 10000000000000000000000000000000000

result = 1
while e > 0:
    if e%2 == 1:
        result = (result * a) % n

    a = (a ** 2) % n
    e //= 2

result %= n
print(f"Result: {result}")