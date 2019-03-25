import numpy as np
import cv2
import socket
import threading
import datetime

msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 46080

class MyThread2(threading.Thread):
    num=0
    def darNombre(self, pnum):
            num=pnum
    def run(self):
        recibidos=0
        inicio=0
        fin=0
        delta=0
        # Create a UDP socket at client side
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Send to server using created UDP socket
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        isRecording=True
        s="".encode('ascii')
        while(True):
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            inicio=datetime.datetime.now().time()
            recibidos=recibidos+1
            print(recibidos)
            try:
                if("{}".format(msgFromServer[0].decode())=="fin"):
                    print("{}".format(msgFromServer[0].decode()))
                    f.write("fin")
                    f.write("Se recibieron: "+str(recibidos)+ " paquetes en el cliente"+num)
                    fin=datetime.datetime.now().time()
                    delta=fin-inicio
                    f.write("Tiempo de atencion cliente: "+str(delta))
                    break
            except:
                pass

        print('cliente '+str(x+1)+' termino')
f=open("UDPClientResults.txt","a+")
for x in range(0,150):
    mythread2= MyThread2()
    numero=str(x+1)
    mythread2.darNombre(numero)
    mythread2.start()
    print('cliente '+str(x+1)+' comenzo')
    #f.write("Cliente %d\r\n" % (x+1))
