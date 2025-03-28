from sympy import nextprime
from random import getrandbits

def binary_pad(num: int, pad_len: int = -1) -> str:
    """
    Converts a number to a binary string, left-padded with zeros to a specified length.

    Args:
        num (int): The number to convert to binary.
        pad_len (int): The target length of the padded binary string (-1 for no padding).

    Returns:
        str: The zero-padded binary string.
    """
    
    value = bin(num)[2:]
    while pad_len > len(value):
        value = "0" + value
    return value

def binary_exponentiation(base:int,exponent:int,modulus:int) -> int:
    """
    Computes (base^exponent) % modulus efficiently using binary exponentiation.

    Args:
        base (int): The base number.
        exponent (int): The exponent.
        modulus (int): The modulus.

    Returns:
        int: The result of (base^exponent) % modulus.
    """

    result = 1

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus

        base = (base ** 2) % modulus
        exponent //= 2

    result %= modulus
    return result

def extended_euclidean_algorithm(exponent:int, modulus:int) -> int:
    """
    Finds the modular multiplicative inverse of `exponent` modulo `modulus` using the extended Euclidean algorithm.

    Args:
        exponent (int): The number for which to find the inverse.
        modulus (int): The Modulus Number.

    Returns:
        int: The modular multiplicative inverse of `exponent` modulo `modulus`.
    """

    a = modulus
    b = exponent

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
        y += max(exponent, modulus)
    
    return y

def generate_keys() -> dict:
    """
    Generates RSA public and private keys.
    
    Returns:
        dict: A dictionary containing:
            - "public" (int): The public exponent.
            - "private" (int): The private exponent.
            - "modulus" (int): The modulus.
    """
    
    p = 0
    q = 0
    
    while p == q:
        p = nextprime(getrandbits(1024))
        q = nextprime(getrandbits(1024))

        if p.bit_length() > 1024 or q.bit_length() > 1024:
            p == q

    n = p * q
    phi = (p-1) * (q - 1)
   
    e = 65537
    d = extended_euclidean_algorithm(e,phi)

    return {"public":e,"private":d,"modulus":n}

def encrypt_message(message:int, public_key:int, modulus:int) -> int:
    """
    Encrypts a message using the RSA encryption algorithm.

    Args:
        message (int): The message represented as an integer.
        public_key (int): The public exponent used for encryption.
        modulus (int): The modulus (part of the public key).

    Returns:
        int: The encrypted message represetned as an integer.
    """
    
    return binary_exponentiation(message,public_key,modulus)

def decrypt_message(message:int, private_key:int, modulus:int) -> int:
    """
    Decrypts a message using the RSA encryption algorithm.

    Args:
        message (int): The encrypted message represented as an integer
        private_key (int): The private exponent used for decryption.
        modulus (int): The modulus (part of the public key).

    Returns:
        int: The decrypted message represetned as an integer.
    """

    return binary_exponentiation(message,private_key, modulus)

def encode_message(message:str) -> int:
    """
    Encodes a message into an integer using ASCII values.

    Args:
        message (str): The message to be encoded.

    Returns:
        int: The message encoded as an integer.
    """
    
    output = 0
    for i, letter in enumerate(message):
        value = ord(letter)
        output += value * (256 ** (len(message) - i - 1))

    return output

def decode_message(encoded_message:int) -> str:
    """
    Decodes a message into a string using ASCII values.

    Args:
        encoded_message (int): The encoded message

    Returns:
        str: The original message as a string.
    """
    
    message = ""
    while encoded_message > 0:
        message =chr(encoded_message%256) + message
        encoded_message //= 256

    return message

def send_keys(keys:dict) -> None:
    """
    Sends the public key and modulus encoded as binary data in a text file.

    Args:
        keys (dict): A dictionary containing RSA keys.
            - "public" (int): The public key
            - "private" (int): The private key
            - "modulus" (int): The modulus
    """
    data = "0" + binary_pad(keys["public"]) + binary_pad(keys["modulus"],2048)
    
    with open("data.txt","w") as file:
        file.write(data)

def send_message(message:str, public_key:int, modulus: int) -> None:
    """
    Sends an encrypted message encoded as binary in a text file.

    Args:
        message (str): The plaintext message to be encrypted and sent.
        public_key (int): Public key used for encryption.
        modulus (int): Modulus used for encryption.
    """    

    data = "1" + binary_pad(encrypt_message(encode_message(message),public_key,modulus),2048)
    
    with open("data.txt","w") as file:
        file.write(data)

def receive_keys() -> dict:
    """
    Recieves the public key and modulus from a text file encoded in binary and return them as a dictionary.

    Returns:
        dict: A dictionary containing:
            - "public" (int): The public key.
            - "modulus" (int): The modulus.
    """
    
    data = ""
    public_key = ""
    modulus = ""

    with open("data.txt","r") as file:
        data = file.read()

    if data[0] == "0":
        public_key = int(data[1:18],2)
        modulus = int(data[18:],2)
    
    return {"public":public_key,"modulus":modulus}

def receive_message(keys: dict) -> str:
    """
    Receives the encrypted message from a text file encoded as binary and returns the decrypted message.

    Args:
        keys (dict): A dictionary containing RSA keys.
            - "public" (int): The public key.
            - "private" (int): The private key.
            - "modulus" (int): The modulus.

    Returns:
        str: The decrypted plaintext message.
    """
    
    data = ""
    message = ""

    with open("data.txt","r") as file:
        data = file.read()

    if data[0] == "1":
        message = decode_message(decrypt_message(int(data[1:],2),keys["private"], keys["modulus"]))

    return message

def main():
    keys = generate_keys()
    send_keys(keys)
    public_keys = receive_keys()
    send_message("This is a message that will be encrypted using RSA!",public_keys["public"],public_keys["modulus"])
    print(f"Message Received: {receive_message(keys)}")

if __name__ == "__main__": main()