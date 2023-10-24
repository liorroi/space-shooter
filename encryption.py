from Crypto.Cipher import AES


def pedd(text):
    if not len(text) % 16 == 0:
        return text + (16 - (len(text) % 16)) * b'\00'
    return text


def encrypt_file(file, key):
    data = file.read()
    print(len(data) % 16)
    size = len(data)
    padded = pedd(data)
    print(len(padded) % 16)
    cipher = AES.new(key.encode(), AES.MODE_CBC)
    encrypted = cipher.encrypt(padded)

    file.write(data)
    print(cipher.iv)
    return cipher.iv ,size


def decrypt_file(file, key, iv, size):
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(file.read())
    return decrypted[:size]

with open('1.bmp', 'rb') as file_name:
    encrypt_file(file_name, key)