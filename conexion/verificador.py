import hashlib
from cryptography.fernet import Fernet
 # Put this somewhere safe!


def encriptar(str):
       file = open('key.key', 'rb')
       key = file.read()  # The key will be type bytes
       file.close()
       message = str.encode()
       f = Fernet(key)
       return f.encrypt(message)


def calcularHash( msj):
        msjs = str(msj)
        h = hashlib.new("sha1",msjs.encode())
        return h.hexdigest()


def encriptarHash(obj):
    return encriptar(calcularHash(obj))
