import socket, select
import hashlib, binascii, os
import persistence as db

if __name__ == "__main__":
	print("main")
	CONEXIONES = []
	BUFFER = 4096
	PORT = 5000
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("localhost", PORT))
	server_socket.listen(10)
	
	CONEXIONES.append(server_socket)
	
	print("Servidor iniciado en el puerto " + str(PORT))
	
	def verify_password(stored_password, provided_password):
		#Verify a stored password against one provided by user
		salt = stored_password[:64]
		stored_password = stored_password[64:]
		pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),salt.encode('ascii'), 100000)
		pwdhash = binascii.hexlify(pwdhash).decode('ascii')
		return pwdhash == stored_password
	
	
	def broadcast(sock,msg):
		for s in CONEXIONES:
			if(s==sock):
				continue
			sock.send(msg)
	allowed_origins = []
	while True:
		read_sockets, write_sockets, error_sockets = select.select(CONEXIONES, [], [])
		
		for sock in read_sockets:

			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				CONEXIONES.append(sockfd)
				print("El cliente (%s, %s) está conectado" %addr)
				
			else:
				status = 0
				print(str(status)+"estado")
				try:
					#sock.send(b"Para iniciar sesion escribe 1, para registrarte escribe 2")
					#if(status==0):
					#	sock.send(b"Para iniciar sesion escribe 1, para registrarte escribe 2")
					data = sock.recv(BUFFER)

					#recibe
					#1 autentica 2 crea
					#llamo mongo
					#si coincide con el metodo verify, emito un mensaje para llamar lo de rafael
					if data:
						#sock.send(data)
						print(data.decode())
						if data.decode()=="1" or data.decode() == "2":
							status = int(data.decode())
							print(str(status)+"estado")

							print(data.decode())
							if status == 1:
								sock.send("Inicio de sesion")
							else:
								sock.send("Registro")
							print("loeoe")
						else:
							if status == 0:
								sock.send("Opcion invalida")
							else:
								if(sock not in allowed_origins):
									sock.send(b"Ingresa tu Username: ")
									username = sock.recv(4096)
									print(username)
									sock.send(b"Password: ")
									pw = sock.recv(4096)
									print(pw)
									if(status == 1):
										usuario = db.getUser(username)
										if(usuario == None):
											sock.send(b"No existe")
										elif (verify_password(usuario.password, pw)):
											sock.send(b"Exito")
											allowed_origins.append(sock)
										else:
											sock.send(b"No es la contrasenia")
									elif status == 2:
										created = db.createUser(username, pw)
										if not created:
											sock.send(b"El usuario ya existe")
											status == 0
										else:
											sock.send(b"Usuario creado")
											status ==0
						
				except:
					print("Client (%s,%s) is offline"%addr)
					sock.close()
					CONEXIONES.remove(sock)
					continue
	server_socket.close()
