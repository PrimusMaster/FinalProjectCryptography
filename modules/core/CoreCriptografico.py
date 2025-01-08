import base64
from Crypto.Util import number
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

def Convert(location):
    with open(location,'r') as f:
        data_key = f.read(70)
        

    with open(location,'rb') as f:
        data = f.read()

    data_key = base64.b64encode(data_key)
    hash = SHA256.new()
    hash.update(data_key)
    key = hash.digest()
    hash = SHA256.new()
    hash.update(key)
    iv = hash.digest(key)
    iv = iv[:128]

    AES.key_size = 256

    cipher = AES.new(key, AES.MODE_CBC, IV= iv)

    EnD = cipher.encrypt(data)

    Encryptedlocation = location.split(".")[0]
    Encryptedlocation = Encryptedlocation + "Encrypted.pem"

    EnD = base64.b64encode(EnD)

    with open(Encryptedlocation, 'wb') as f:
        f.write(EnD)


def convert_decrypt(location, location_encrypted):
    with open(location,'r') as f:
        data_key = f.read(70)
    
    with open(location_encrypted,'rb') as f:
        data = f.read()
        data = base64.b64decode(data)

    data_key = base64.b64encode(data_key)
    hash = SHA256.new()
    hash.update(data_key)
    key = hash.digest()
    hash = SHA256.new()
    hash.update(key)
    iv = hash.digest(key)
    iv = iv[:128]


    AES.key_size = 256

    cipher = AES.new(key, AES.MODE_CBC, IV= iv)

    DeD = cipher.decrypt(data)

    Encryptedlocation = location.split(".")
    Encryptedlocation = Encryptedlocation[0] + "_Decrypted" + Encryptedlocation[1]
    

    with open(Encryptedlocation, 'w') as f:
        f.write(DeD)



def ECDSA_keygeneration(Password,username):
    mykey = ECC.generate(curve='p256')
    pwd = Password.encode()
    with open("../storage/users/myprivatekey"+username+".pem", "wt") as f:
        data = mykey.export_key(format='PEM',
                                passphrase=pwd,
                                protection='PBKDF2WithHMAC-SHA512AndAES256-CBC',
                                prot_params={'iteration_count':131072})
        f.write(data)
    with open("../storage/users/mypublickey"+username+".pem", "wt") as f:
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
        infoToSign = f.read()
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

def HASH(Text: str):
    hash = SHA256.new()
    result = hash.update(base64.b64encode(Text.encode()))
    return base64.b64decode(result).decode()


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
    ECDSA_keygeneration("hola", "Pepe")
    #main()
