import socket
import sys
import functions
import time
# Create a TCP/IP socket
loop = True
while(loop):
        sock = socket.create_connection(('localhost', 10000))
        try:

            # Send data
            print("Ingrese sus valores 'p','g' y 'a'... ")
            print("----------------------------------------")
            time.sleep(2)
            entero = 0
            while(entero == 0):
                try: 
                    p = int(input("Su valor de p: "))
                    while (not functions.validacion_1(p)):
                        print("Ingrese un valor correcto de p \n (Este debe ser un numero primo)...")
                        print("----------------------------------------")
                        time.sleep(2)
                        p = int(input("Su valor de p: "))
                    g = int(input("Su valor de g: "))
                    while (not functions.validacion_2(g,p)):
                        print("Ingrese un valor correcto de g \n (Este debe ser un numero mayor a 0 y menor al p ingresado)...")
                        print("----------------------------------------")
                        time.sleep(2)
                        g = int(input("Su valor de g: "))
                    a = int(input("Su valor de a: "))
                    while (not functions.validacion_3(a,p)):
                        print("Ingrese un valor correcto de a \n (Este debe ser un numero mayor a 0 y menor a p-1)...")
                        print("----------------------------------------")
                        time.sleep(2)
                        a = int(input("Su valor de a: "))
                    entero = 1
                except ValueError:
                    print("Sus valores deben ser enteros positivos (ej: 3,7,320)")
                    print("----------------------------------------")
                    time.sleep(2)
            valorA = functions.Calculo(a,g,p)
            index = 0
            g = g.to_bytes(2,'big')
            p = p.to_bytes(2,'big')
            valorA =valorA.to_bytes(2,'big')
            lista = [g,p,valorA]
            while (index<3):
                sock.sendall(lista[index])
                amount_received = 0
                amount_expected = len(g)

                while amount_received < amount_expected:
                    data = sock.recv(16)
                    amount_received += len(data)
                index = index + 1
            recibido = sock.recv(1024)
            recibido = int.from_bytes(recibido,byteorder='big')
            print(f"Su variable B es: {recibido}")
            print("----------------------------------------")
            time.sleep(2)


            g_converted = int.from_bytes(g,byteorder='big')
            p_converted = int.from_bytes(p,byteorder='big')

            valorKB = functions.Calculo(a,recibido,p_converted)
            print(f"el valor de K obtenido es: {valorKB}")
            print("----------------------------------------")
            time.sleep(2)
            valorKB_by = valorKB.to_bytes(2,'big')
            sock.send(valorKB_by)
            data = sock.recv(16)
            valorKA = int.from_bytes(data,byteorder='big')
            if valorKA == valorKB:
                print("Usted esta conectado con el servidor de manera segura!")
                print("----------------------------------------")
                time.sleep(2)
                Texto = input('Ingrese el mensaje que desee enviar al servidor: ')
                print("----------------------------------------")
                msj_en= open('mensajeentrada.txt', 'a')
                print("Encriptando mensaje...")
                print("----------------------------------------")
                time.sleep(2)
                print(f"Mensaje escrito en el fichero de entrada: {Texto}")
                msj_en.write(Texto + '\n')
                msj_en.close()
                message = b'ok'
                print("----------------------------------------")
                time.sleep(2)
                sock.send(message)
                time.sleep(20)
            else: 
                print("No se ha podido conectar con el servidor")
                print("----------------------------------------")
                time.sleep(2)
        finally:
            print('Se cierra el socket')
            print("----------------------------------------")
            time.sleep(2)
            sock.close()
