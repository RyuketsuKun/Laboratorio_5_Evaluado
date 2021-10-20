from io import TextIOWrapper
from typing import TextIO
from Crypto.Cipher import DES
from Crypto.Cipher import DES3
from Crypto.Cipher import AES
def validacion_1 (p):
    if p < 1:
        return False
    elif p == 2:
        return True
    else:
        for i in range(2, p):
            if p % i == 0:
                return False
        return True


def validacion_2 (g,p):
    if g <= 0:
        return False
    elif g >= p:
        return False
    else:
        return True


def validacion_3 (a,p):
    if a <= 0:
        return False
    elif a >= (p-1):
        return False
    else:
        return True


def Calculo (privado,publico1,publico2):
    elevacion = publico1 ** privado
    modulo = elevacion % publico2
    return modulo





#Apartado DES
def encrypt(msg,llave):
    cipher = DES.new(llave, DES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
    return nonce, ciphertext, tag

def decrypt(nonce, ciphertext, tag,llave):
    cipher = DES.new(llave, DES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)

    try:
        cipher.verify(tag)
        return plaintext.decode('ascii')
    except:
        return False


#Apartado 3DES
def encrypt3DES(msg,llave):
    cipher = DES3.new(llave,DES3.MODE_EAX)
    nonce = cipher.nonce
    textocifrado = cipher.encrypt(msg.encode('ascii'))
    return nonce, textocifrado


def decrypt3DES(nonce,textocifrado,llave):
    cipher = DES3.new(llave, DES3.MODE_EAX, nonce=nonce)
    textoplano = cipher.decrypt(textocifrado)
    return textoplano.decode('ascii')
    


#ApartadoAES
def encryptAES(msg,llave):
    cipher = AES.new(llave,AES.MODE_EAX)
    nonce = cipher.nonce
    textocifrado, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
    return nonce, textocifrado, tag


def decryptAES(nonce, textocifrado, tag,llave):
    cipher = AES.new(llave, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(textocifrado)
    try:
        cipher.verify(tag)
        return plaintext.decode('ascii')
    except:
        return False

