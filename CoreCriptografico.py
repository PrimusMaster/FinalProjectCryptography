import base64
from Crypto.Util import number
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.PublicKey import ECC
from Signature import eddsa

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

def ECDSA_keygeneration(Password):
    mykey = ECC.generate(curve='p256')
    pwd = Password.encode()
    with open("myprivatekey.pem", "wt") as f:
        data = mykey.export_key(format='PEM'
                                    passphrase=pwd,
                                    protection='PBKDF2WithHMAC-SHA512AndAES256-CBC',
                                    prot_params={'iteration_count':131072})
        f.write(data)
    with open("mypublickey.pem", "wbt") as f:
        data = mykey.public_key().export_key()

def ECDSA_Signature(privatekeylocation,publickeylocation):
    pwd = b'secret'
    with open("myprivatekey.pem", "rt") as f:
        data = f.read()
        mykey = ECC.import_key(data, pwd)


def ECDSA_Verification():
    message = b'I give my permission to order #4355'
    key = ECC.import_key(open('privkey.der').read())
    h = SHA256.new(message)
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(h)

def main():
    print("Escoja alguna de las siguientes opciones:")
    print(
    """
    1.-Encriptar con llave comun
    2.-Encriptar con llave publica
    4.-Desencriptar con llave privada
    3.-Salir
    """
    )
    opcion = input()
    while True:
        if opcion == "1":
            print("ingrese el nombre del archivo:")
            Direccion = input()
            Convert(Direccion) 
        elif opcion == "2":





if ___name___ == '___main___':
    main()