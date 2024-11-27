import base64
from Crypto.Util import number
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def Convert(location):
    with open(location,'r') as f:
        data_key = f.read()
        iv_data = data_key [:50]

    with open(location,'rb') as f:
        data = f.read()

    data_key = base64.b64encode(data_key)
    iv_data = base64.b64encode(iv_data)
    hash = SHA256.new()
    key = hash.update(data_key)
    iv = hash.update(iv_data)
    AES.key_size = 256

    cipher =  AES.new(key,mode= AES.MODE_CBC, IV= iv)

    Encryptedlocation = location.split(".")[0]
    Encryptedlocation = Encryptedlocation + "Encrypted.pem"

    ED = cipher.encrypt(pad(data, AES.block_size))

    ED = base64.b64encode(ED).decode('utf-8')

    with open(Encryptedlocation, 'wb') as f:
        f.write(ED)

    


def main():


if ___name___ == '___main___':
    main()