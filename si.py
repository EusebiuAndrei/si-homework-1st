from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

key = "abcdefghabcdefgh".encode('utf-8')  # get_random_bytes(16)
ecb_key = "abcdefghabcdefgh".encode('utf-8')
ofb_key = "abcdefghabcdefgh".encode('utf-8')
iv = 'aaaaaaaaaaaaaaaa'.encode('utf-8')
# cipher = AES.new(key, AES.MODE_ECB)


def byte_xor(ba1, ba2):
    """ XOR two byte strings """
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def aes_basic_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    # print("A", data)
    # data = pad(data, AES.block_size)
    # print("B", data)
    data = cipher.encrypt(data)
    # print("C", data)
    return data


def aes_basic_decrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_bytes = cipher.decrypt(data)
    # return unpad(decrypted_bytes, AES.block_size)
    return decrypted_bytes


def ecb_encrypt(data, key):
    encryptions = []
    data = pad(data, AES.block_size)

    for i in range(0, len(data), AES.block_size):
        chunk = data[i:i + AES.block_size]
        encrypted = aes_basic_encrypt(chunk, key)
        encryptions.append(encrypted)

    return encryptions


def ecb_decrypt(encryptions, key):
    plaintext = ''

    for encrypted in encryptions:
        plaintext += aes_basic_decrypt(encrypted, key).decode('utf-8')

    return unpad(plaintext.encode('utf-8'), AES.block_size).decode('utf-8')


def ofb_encrypt(data, key):
    encryptions = []
    feedback = iv
    data = pad(data, AES.block_size)

    for i in range(0, len(data), AES.block_size):
        chunk = data[i:i + AES.block_size]
        feedback = aes_basic_encrypt(feedback, key)
        encrypted = byte_xor(feedback, chunk)
        encryptions.append(encrypted)

    return encryptions


def ofb_decrypt(encryptions, key):
    plaintext = ''
    feedback = iv
    some = []

    for encrypted in encryptions:
        feedback = aes_basic_encrypt(feedback, key)
        decrypted = byte_xor(feedback, encrypted)
        plaintext += decrypted.decode('utf-8')
        some.append(decrypted)

    return unpad(plaintext.encode('utf-8'), AES.block_size).decode('utf-8')


def try_decrypt(encryptions):
    plaintext = ''
    feedback = iv
    some = []

    for encrypted in encryptions:
        feedback = aes_basic_encrypt(feedback)
        decrypted = byte_xor(feedback, encrypted)
        some.append(decrypted)

    print("AOLEU", some)
    return ''


if __name__ == '__main__':
    data = "secret john marry get some apples funny"
    print(AES.block_size)

    # a = ecb_encrypt(data.encode('utf-8'))
    # print(a)
    # print(ecb_decrypt(a))
    # print()
    c = ofb_encrypt(data.encode('utf-8'))
    print(c)
    print()
    print(ofb_decrypt(c))