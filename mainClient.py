import socket, select, string, sys
import hashlib, binascii, os


def prompt():
	sys.stdout.write('<you>')
	sys.stdout.flush()

def hash_password(password):
    #Hash a password for storing.
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
	
if __name__ == "__main__":
		
	host = "localhost"
	port = 5000
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(3)
	
	try:
		s.connect((host, port))
	except:
		print("No se ha podido conectar al servidor")
		sys.exit()
	
	print("Conectado al servidor" + hash_password("hola"))
	print("Para iniciar sesion escribe 1, para registrarte escribe 2")
	prompt()
	
	while True:
		socket_list = [sys.stdin, s]
		
		read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
		
		for sock in read_sockets:
			if sock == s:
				data = sock.recv(4096)
				if not data:
					print ("Desconexion")
					sys.exit()
				else:
					sys.stdout.write(data.decode())
					prompt()
			else:
				msg = sys.stdin.readLine()
				s.send(msg.encode())
				prompt()