import socket
import cv2
import threading

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 46080
addresses=[]
connections=[]

#Se crea el socket TCPdel servidor
TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

#Se inicia escuchar peticiones en el puerto localPort
TCPServerSocket.bind((localIP, localPort))
TCPServerSocket.listen(150)

#se inicia la captura del video a transmitir
cap = cv2.VideoCapture('bebecita.mp4')

class MyThread2(threading.Thread):
    def run(self):
        while(True):
            #se toma un nuevo frame del video
            rep, frame = cap.read()
            if rep == True:
                for i in range(20):
                    print(i)
                    for conn in connections:
                        #se dividen los frames en paquetes que se transmiten a todas las direcciones de los clientes conectados
                        conn.sendall(frame.flatten().tostring()[i*46080:(i+1)*46080])
            else:
                break

print("TCP server up and listening")   

# Se crea un hilo que enviara capturas a los clientes conectados
mythread2 = MyThread2() 
mythread2.start()  

while True:
    #Se reciben nuevas conexiones con clientes y se añaden a las direcciones a las cual se transmitira el video
    bytesAddressPair = TCPServerSocket.accept()
    conn = bytesAddressPair[0]
    address= bytesAddressPair[1]
    mythread2.isAlive()
    print(address)
    if address not in addresses:
        connections.append(conn)
