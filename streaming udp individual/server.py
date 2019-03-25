import socket
import cv2
import threading

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 46080

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)
global addresses
addresses=[]
global vid
vid=[]
global kkk
kkk=False


#Se crea el socket udp del servidor
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Se inicia escuchar peticiones en el puerto localPort
UDPServerSocket.bind((localIP, localPort))

#se inicia la captura del video a transmitir
global cap 
cap = cv2.VideoCapture('med.mp4')

def nuevoVid(idVid):
    global cap
    print(idVid)
    if idVid=='1':
        cap = cv2.VideoCapture('bh.mp4')
    elif idVid=='2':
        cap = cv2.VideoCapture('peq.mp4')
    elif idVid=='3':
        cap = cv2.VideoCapture('med.mp4')    

class MyThread2(threading.Thread):
    def run(self):
        while(True):
            global kkk
            if kkk:      
                #se toma un nuevo frame del video
                rep, frame = cap.read()
                if rep == True:
                    for i in range(20):
                        for ad in addresses:
                            #se dividen los frames en paquetes que se transmiten a todas las direcciones de los clientes conectados
                            UDPServerSocket.sendto(frame.flatten().tostring()[i*46080:(i+1)*46080], ad)
                else:
                    kkk=False
                    print('finVid')
            else:
                print(kkk)
                if len(vid)>0:
                    print('inicioVid')
                    print(vid)
                    nuevoVid(vid.pop())
                    kkk=True

print("UDP server up and listening")   

# Se crea un hilo que enviara capturas a los clientes conectados
mythread2 = MyThread2() 
mythread2.start()  

while True:
    #Se reciben nuevas conexiones con clientes y se añaden a las direcciones a las cual se transmitira el video
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    vid=bytesAddressPair[0].decode().split(',')
    address = bytesAddressPair[1]
    mythread2.isAlive()
    print(address)
    if address not in addresses:
        addresses.append(address)
