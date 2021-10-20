import socket
import sys
import functions
import random
import time
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from secrets import token_bytes
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('Iniciando servidor {} en el puerto {}'.format(*server_address))
print("----------------------------------------")
time.sleep(2)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
while True:
    # Wait for a connection
    print('Esperando una conexion...')
    print("----------------------------------------")
    time.sleep(2)
    connection, client_address = sock.accept()
    try:
        print('conexion realizada desde: ', client_address)
        print("----------------------------------------")
        time.sleep(2)
        # Receive the data in small chunks and retransmit it
        index = 0
        datos = []
        while (index<3):
            data = connection.recv(16)

            if data:
                if index == 0:
                    connection.sendall(data)
                    g = int.from_bytes(data,byteorder='big')
                    datos.append(g)
                    index = index + 1
                elif index == 1:
                    connection.sendall(data)
                    p = int.from_bytes(data,byteorder='big')
                    datos.append(p)
                    index = index + 1
                else:
                    connection.sendall(data)
                    valorA = int.from_bytes(data,byteorder='big')
                    print(f"Su valor A es: {valorA}")
                    print("----------------------------------------")
                    time.sleep(2)
                    datos.append(valorA)
                    index = index + 1
            else:
                print('no data from', client_address)
                print("----------------------------------------")
                time.sleep(2)
                break
        b = random.randint(1,datos[0])
        print(f"El valor de b elegido por el servidor es: {b}")
        print("----------------------------------------")
        time.sleep(2)
        valorB =functions.Calculo(b,datos[0],datos[1])
        valorB = valorB.to_bytes(2,'big')
        connection.send(valorB)
        print("Valor de B enviado al cliente...")
        print("----------------------------------------")
        time.sleep(2)
        valorKA = functions.Calculo(b,datos[2],datos[1])
        print(f"el valor de K obtenido es: {valorKA}")
        print("----------------------------------------")
        time.sleep(2)
        valorKA_by = valorKA.to_bytes(2,'big')
        connection.send(valorKA_by)
        data = connection.recv(16)
        valorKB = int.from_bytes(data,byteorder='big')
        if valorKB == valorKA:
            print("El servidor esta conectado con el cliente de manera segura!")
            print("----------------------------------------")
            time.sleep(2)
            data = connection.recv(16)
            if data == (b'ok'):
                textocifrado =  connection.recv(10000)
                msj_en =open('mensajeentrada.txt', 'r')
                for linea in msj_en.readlines():
                    if linea[-1] =="\n":
                        linea = linea[:-1]
                valorKB = valorKB.to_bytes(8,'big')
                nonce, ciphertext, tag = functions.encrypt(linea,valorKB)
                print(f"Exito!, su mensaje escrito fue: {ciphertext}")
                print("----------------------------------------")
                plaintext = functions.decrypt(nonce, ciphertext, tag,valorKB)
                msj_en.close()
                time.sleep(2)
                print("Desencriptando...")
                print(f"Exito!, su mensaje escrito fue: {plaintext}")
                print("----------------------------------------")
                time.sleep(2)
                msj_sal = open('mensajerecibido.txt', 'a')
                msj_sal.write(plaintext + '\n')
                msj_sal.close()
                print("Guardando texto en archivo txt")
                print("----------------------------------------")


                #Apartado 3DES


                time.sleep(2)
                print("Encriptando en 3DES")
                print("----------------------------------------")
                time.sleep(2)
                aux = True
                while aux:
                    try:
                        llave = DES3.adjust_key_parity(get_random_bytes(24))
                        break
                    except ValueError:
                        pass
                nonce3, textocifrado3 = functions.encrypt3DES(plaintext,llave)
                print(f"Exito!, su mensaje escrito fue: {textocifrado3}")
                print("----------------------------------------")
                time.sleep(2)
                print("Desencriptando...")
                print("----------------------------------------")
                time.sleep(2)
                textocifrado3 = functions.decrypt3DES(nonce3,textocifrado3,llave)
                print(f"Exito!, su mensaje escrito fue: {textocifrado3}")
                print("----------------------------------------")
                time.sleep(2)


                #Apartado AES
                print("Encriptando en AES")
                print("----------------------------------------")
                time.sleep(2)
                llave = token_bytes(16)
                nonceAES, textocifradoAES, tagAES = functions.encryptAES(textocifrado3,llave)
                print(f"Exito!, su mensaje escrito fue: {textocifradoAES}")
                print("----------------------------------------")
                time.sleep(2)
                print("Desencriptando...")
                print("----------------------------------------")
                time.sleep(2)
                textocifradoAES = functions.decryptAES(nonceAES,textocifradoAES,tagAES,llave)
                print(f"Exito!, su mensaje escrito fue: {textocifradoAES}")
                print("----------------------------------------")
                time.sleep(2)







        else: 
            print("No se ha podido conectar con el cliente")
            print("----------------------------------------")
            time.sleep(2)
    finally:
        # Clean up the connection
        connection.close()