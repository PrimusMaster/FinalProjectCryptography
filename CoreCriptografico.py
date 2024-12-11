import base64
from Crypto.Util import number
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

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
        data = mykey.export_key(format='PEM',
                                passphrase=pwd,
                                protection='PBKDF2WithHMAC-SHA512AndAES256-CBC',
                                prot_params={'iteration_count':131072})
        f.write(data)
    with open("mypublickey.pem", "wt") as f:
        data = mykey.public_key().export_key(format='PEM')
        f.write(data)

def ECDSA_Signature(Password,privatekeylocation,documentlocation):
    pwd = Password.encode()
    with open(privatekeylocation, "rt") as f:
        data = f.read()
        mykey = ECC.import_key(data, pwd)
    with open(documentlocation,"rb") as f:
        infoToSign =  f.read()
        h = SHA256.new(infoToSign)
    signer = DSS.new(mykey, 'fips-186-3')
    firma = signer.sign(h)
    firma64 = base64.b64encode(firma)
    with open("Firma.txt","wb") as f:
        f.write(firma64)
    
    

def ECDSA_Verification(publickeylocation,documentlocation,signaturelocation):
    key = ECC.import_key(open(publickeylocation).read())
    with open(documentlocation,"rb") as f:
        infoToSign =  f.read()
        h = SHA256.new(infoToSign)
    verifier = DSS.new(key, 'fips-186-3')
    with open(signaturelocation,"rb") as f:
        signature = f.read()
        signature = base64.b64decode(signature)
    try:
        verifier.verify(h, signature)
        print("The message is authentic.")
    except ValueError:
        print("The message is not authentic.")

def HASH(Text):
    hash = SHA256.new()
    result = hash.update(Text)
    return result


def main():
    
    while True:
        print("Escoja alguna de las siguientes opciones:")
        print(
        """
        1.-Crear llaves
        2.-Firmar documento
        3.-Verificar firma
        5.-Salir
        
        """
        )
        opcion = input()

        if opcion == "1":
            print("ingrese una contraseña:")
            Password = input()
            ECDSA_keygeneration(Password) 
        elif opcion == "2":
            print("ingrese la contraseña:")
            Password = input()
            ECDSA_Signature(Password,"myprivatekey.pem","Prueba.txt")
        elif opcion == "3":
            ECDSA_Verification("mypublickey.pem","Prueba.txt","Firma.txt")
        elif opcion == "5":
            break





if __name__ == '__main__':
    main()