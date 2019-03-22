import socket, select, sys
import hashlib, binascii, os
import json
from _thread import *

host = ''
port = 8082

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

	
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host,port))
except socket.error:
	print("No se pudo desplegar el servidor")
	sys.exit()

print("Despliegue correcto del servidor")
s.listen(1000)
print("Servidor listo")


def threadCliente(conn):
	conn.send("sapo")
	while 1:
		data = conn.recv(1024)
		reply = "OK"
		if not data:
			break;
		conn.sendall(reply)
	conn.close()




while 1:
	conn, addr = s.accept()
	print("Conectado con " + addr[0] + ":" + str(addr[1]))
	start_new_thread(threadCliente, (conn,))