e = 17
phi = 3120

a = phi
b = e

r = a % b
quotients = []

while r > 0:
    quotients.append(a//b)
    
    a = b
    b = r
    r = a%b

x = 1
y = -quotients[-1]

for i in range(len(quotients)-1):
    t = x
    x = y
    y = t - (quotients[-(i + 2)] * y)

if y < 0:
    y += phi

print(f"e = {e}")
print(f"d = {y}")
print(f"phi = {phi}")
print(f"(e * d) mod phi = 1: {(e * y)%phi == 1}")