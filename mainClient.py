
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

	print("Para iniciar sesion escribe 1, para registrarte escribe 2")
	prompt()
	
	status = 0
	
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
				
				msg = input()
				s.send(msg.encode())
				resp = s.recv(4096)
				print("llego respuesta")
				print(resp)
				if(resp.decode()=="Ya iniciaste sesion"):
					print("Bienvenido")
					break
				if(resp.decode()== "Password: "):
					pw = input()
					print(hash_password(pw))
					s.send(hash_password(pw).encode())
					auth = s.recv(4096)
					if(auth.decode() == "No existe"):
						print("Fallo en la autenticacion")
					elif(auth.decode() == "No es la contrasenia"):
						print("Contrasenia incorrecta")
					else:
						print("Bienvenido!")
						break
				else:
					continue
				prompt()
