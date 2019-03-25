
import socket, select, string
import threading, datetime

#Se definen las caracteristicas basicas del socket donde se quiere conectar: Puerto, host, y protocolo (TCP=SOCK_STREAM)
hostInfo = ("localhost",5000)
buffer = 4096
testUser = "juanEspitia"
testPassword = "jsRocks"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)


class MyThread2(threading.Thread):
    num=0
    def darNombre(self, pnum):
            num=pnum
    def run(self):
        recibidos=0
        inicio=datetime.datetime.now().time()
        fin=0
        delta=0
        # Create a TCP socket at client side
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#Se intenta establecer una conexion con el socket servidor
		try:
			s.connect(hostInfo)
		except:
			print("No se ha podido conectar al servidor")
			sys.exit()
		s.send(b"1")
		a=s.recv(buffer)
		s.send(testUser.encode())
		b=s.recv(buffer)
		s.send(testPassword.encode())

		c = s.recv(buffer)
		if(c == "Bienvenido"):
			print("auth success")
		fin = datetime.datetime.now().time()
        
f=open("TCPClientResults.txt","a+")
for x in range(0,5):
    mythread2= MyThread2()
    numero=str(x+1)
    mythread2.darNombre(numero)
    mythread2.start()
    print('cliente '+str(x+1)+' comenzo')
    #f.write("Cliente %d\r\n" % (x+1))



