import hashlib
from cryptography.fernet import Fernet
 # Put this somewhere safe!


def encriptar(hash):
       file = open('key.key', 'rb')
       key = file.read()  # The key will be type bytes
       file.close()
       message = hash.encode()
       f = Fernet(key)
       #print ("message Fernet:", message)
       return f.encrypt(message)


def calcularHash( msj):
        msjs = str(msj)
        h = hashlib.new("sha1",msjs.encode())
        print("HASH CALCULADO:",h.hexdigest())
        return h.hexdigest()


def encriptarHash(obj):
    return encriptar(calcularHash(obj))
