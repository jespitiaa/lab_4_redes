import numpy as np
import cv2
import socket

msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 46080

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

isRecording=True
s="".encode('ascii')
while(True):
    data, addr = UDPClientSocket.recvfrom(bufferSize)
    s = s+data
    if len(s)==(46080*20):
        
        frame = np.fromstring(s, dtype='uint8')
        frame = frame.reshape(480, 640, 3)
        s="".encode('ascii')
        if(isRecording):#read the boolean to decide whether to write frame or not
            cv2.imshow('frame', frame)
        # & 0xFF is required for a 64-bit system
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('p'):#Pause
            print('Pause')
            isRecording=False
        if cv2.waitKey(1) & 0xFF == ord('c'):#Continue
            print('Continue')
            isRecording=True
cap.release()
cv2.destroyAllWindows()