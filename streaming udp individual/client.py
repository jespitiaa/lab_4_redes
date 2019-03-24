import numpy as np
import cv2
import socket

msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 46080

# Se crea un socket udp cliente
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# se envia un mensaje al servidor para comenzar la conexion
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

isRecording=True
s="".encode('ascii')
while(True):
    #se reciven los paquetes transmitidos por el servidor
    data, addr = UDPClientSocket.recvfrom(bufferSize)
    #se concatenan los paquetes para formar threads
    s = s+data
    if len(s)==(46080*20):
        #se forma el frame
        frame = np.fromstring(s, dtype='uint8')
        frame = frame.reshape(480, 640, 3)
        s="".encode('ascii')
        if(isRecording):
            cv2.imshow('frame', frame)#se muestra el frame generado
        if cv2.waitKey(1) & 0xFF == ord('q'):#parar transmision
            break
        if cv2.waitKey(1) & 0xFF == ord('p'):#Pause
            print('Pause')
            isRecording=False
        if cv2.waitKey(1) & 0xFF == ord('c'):#Continue
            print('Continue')
            isRecording=True
cap.release()
cv2.destroyAllWindows()