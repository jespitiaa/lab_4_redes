import socket, select, sys
import hashlib, binascii, os
import json

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')



def autenticarme(user, password):
	message = {
		"user" : user,
		"pw" : hash_password(password)
	}
	try:
		s.sendall(json.dumps(message).encode())
	except:
		print("Error al enviar las credenciales")
	reply = s.recv(4096).decode()
	return reply


#Crear conexion
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print("No se pudo establecer conexión")
	sys.exit()
	
print("Se creo el socket")

host = ''
port = 8082

try: 
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print("Hostname no resuelto")
	sys.exit()
	
print("Direccion ipv4: "+ str(remote_ip))

s.connect((remote_ip, port))

print("Se establecio una conexion con " + host)

