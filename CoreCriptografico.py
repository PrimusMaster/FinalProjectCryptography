import base64
from Crypto.Util import number
from Crypto.Hash import SHA256
from Crypto.Cipher import AES


def Convert(location):
    with open(location,'r') as f:
        data = f.read()

    data = base64.b64encode(data)
    hash = SHA256.new()
    key = hash.update(data)

    AES.key_size = 256

    AES.new(key,mode= AES.MODE_CBC,)

def main():


if ___name___ == '___main___':
