import socket
import cv2
import threading
import time

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 46080

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)
addresses=[]

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

cap = cv2.VideoCapture('peq.mp4')
f=open("UDPServerResults.txt","a+")
class MyThread2(threading.Thread):
    def run(self):
        inicio=0
        fin=0
        trans=0
        time.sleep(2)
        enviados=0
        while(True):
            rep, frame = cap.read()
            print(rep)
            # Sending a reply to client
            if rep == True:
                inicio=time.time()
                for i in range(20):
                    for ad in addresses:
                        UDPServerSocket.sendto(frame.flatten().tostring()[i*46080:(i+1)*46080], ad)
                    enviados=enviados+1
                print(str(enviados))
                        #print(str(rep))
            else:
                for ad in addresses:
                    UDPServerSocket.sendto(str.encode("fin"), ad)
                    fin=time.time()
                    trans=fin-inicio
                    print("termino cliente"+ str(ad))
                    f.write("Se enviaron: "+str(enviados)+" paquetes a direccion: "+str(ad)+" Tiempo de transmision de "+str(trans)+"\r\n")
                print('fin todos')
                break

print("UDP server up and listening")

mythread2 = MyThread2()
mythread2.start()

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    address = bytesAddressPair[1]
    print(mythread2.isAlive())
    print(address)
    if address not in addresses:
        addresses.append(address)



print('hola')
# Listen for incoming datagrams
