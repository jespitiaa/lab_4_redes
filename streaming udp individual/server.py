import socket
import cv2
import threading

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 46080

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)
addresses=[]

#Se crea el socket udp del servidor
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Se inicia escuchar peticiones en el puerto localPort
UDPServerSocket.bind((localIP, localPort))

#se inicia la captura del video a transmitir
cap = cv2.VideoCapture('bebecita.mp4')

class MyThread2(threading.Thread):
    def run(self):
        while(True):
            #se toma un nuevo frame del video
            rep, frame = cap.read()
            if rep == True:
                for i in range(20):
                    for ad in addresses:
                        #se dividen los frames en paquetes que se transmiten a todas las direcciones de los clientes conectados
                        UDPServerSocket.sendto(frame.flatten().tostring()[i*46080:(i+1)*46080], ad)
            else:
                break

print("UDP server up and listening")   

# Se crea un hilo que enviara capturas a los clientes conectados
mythread2 = MyThread2() 
mythread2.start()  

while True:
    #Se reciben nuevas conexiones con clientes y se añaden a las direcciones a las cual se transmitira el video
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    address = bytesAddressPair[1]
    mythread2.isAlive()
    print(address)
    if address not in addresses:
        addresses.append(address)
