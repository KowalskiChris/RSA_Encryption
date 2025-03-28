message = "This is a message"
output = 0

for i, letter in enumerate(message):
    value = ord(letter)
    output += value * (256 ** (len(message) - i - 1))

print(f"Binary Message: {bin(output)[2:]}")
print(f"Encoded Message: {output}")

output_message = ""
while output > 0:
    output_message =chr(output%256) + output_message
    output //= 256

print(f"Decoded Message: {output_message}")