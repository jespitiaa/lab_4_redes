import socket, select, numpy
import hashlib, binascii, os
import persistence as db

if __name__ == "__main__":
	#Se tendra un conjunto de sockets conectados
	CONEXIONES = []

	#Se define un tamanio para el buffer de lectura de 4096b, y el puerto de escucha
	BUFFER = 4096
	PORT = 5000
	
	#Se definen caracteristicas basicas del servidor y se despliega en un puerto definido
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("localhost", PORT))
	server_socket.listen(200)
	
	CONEXIONES.append(server_socket)
	
	print("Servidor iniciado en el puerto " + str(PORT))
	
	#Este metodo se va a encargar de verificar un par de contrasenias encriptadas 
	def verify_password(stored_password, provided_password):
		#Verify a stored password against one provided by user
		salt = stored_password[:64]
		stored_password = stored_password[64:]
		pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),salt.encode('ascii'), 100000)
		pwdhash = binascii.hexlify(pwdhash).decode('ascii')
		return pwdhash == stored_password

	#Este metodo va a encriptar la contraseña que el usuario ingrese, de tal forma que al enviarse por el socket, si es interceptada, que no sea legible
	def hash_password(password):
		#Hash a password for storing.
		salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
		pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
									salt, 100000)
		pwdhash = binascii.hexlify(pwdhash)
		return (salt + pwdhash).decode('ascii')

	#El arreglo va a indicar cuales sockets ya se autenticaron		
	allowed_origins = []
	socket_status = [0]
	print(type(socket_status))
	while True:
		#Se guardan variables en arreglos para los sockets y el estado de cada uno (Empieza en 0 para todos)
		read_sockets, write_sockets, error_sockets = select.select(CONEXIONES, [], [])

		for sock in read_sockets:
			username = ""
			pw = ""
 
			#Acepta constantemente nuevas conexiones al servidor
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				if len(CONEXIONES) < 200
					CONEXIONES.append(sockfd)
					socket_status.append(0)
					print("El cliente (%s, %s) está conectado" %addr)
				
			#Lee constantemente informacion enviada desde los clientes en la terminal	
			else:
				index = CONEXIONES.index(sock)
				status = socket_status[index]
				#print(str(status)+" estado")
				#Define el flujo de informacion
				try:
					#Empieza recibiendo informacion del cliente
					data = sock.recv(BUFFER)

					#1 autentica 2 crea
					#llamo mongo
					#si coincide con el metodo verify, emito un mensaje para llamar lo de rafael
					#Revisa si existe un cliente que envie informacion efectivamente 
					if data:
						#sock.send(data)
						print(data.decode(), type(data.decode()))

						#Se pregunta por la primera entrada posible, elegir entre login y registro
						if status == 0 and (data.decode().strip()=="1" or data.decode().strip() == "2") :
							#se cambia el estado 
							status = int(data.decode())
							print(str(status)+"-estado")
							socket_status[index]= status
							sock.send(b"Ingresa tu Username: ")
						#Se recibio el nombre del usuario
						elif data.decode().startswith('user:'):
							username = data.decode().split(":")[1]
							#Se consulta si el usuario ya esta en la base de datos
							print(username)
							usuario = db.getUser(username)
							print(usuario)
							#Caso de inicio de sesion
							if status == 1:
								#El usuario ya debe existir para pedir la contrasenia. Si no existe, se indica al usuario
								if usuario == None:
									print("busca")
									status = 0
									print(str(status)+"-estado")
									socket_status[index]= status
									sock.send(b"Usuario no existe")
								else:
									print("contrasenia")
									sock.send(b"Password: ")
							#Caso de registro
							elif status == 2:
								#El usuario no debe existir para crear uno con la contrasenia que indique el usuario. Si ya existe se avisa
								if usuario == None:
									sock.send(b"Password: ")
								else:
									status = 0
									print(str(status)+"-estado")
									socket_status[index]= status
									sock.send(b"Usuario ya existe")
						
						#Se recibio la contrasenia
						elif data.decode().startswith('password:'):
							pw = data.decode().split(":")[1]
							#Si esta iniciando sesion, se debe validar que las credenciales coincidan
							if(status==1):
								usuario = db.getUser(username)
								if verify_password(usuario.password, pw):
									sock.send(b"Bienvenido")
									allowed_origins.append(sock)
								else:
									sock.send(b"Credenciales incorrectas")
							#Si esta registrandose, se crea un usuario con las credenciales indicadas y se inicia la sesion de forma automatica
							elif(status==2):
								#Crea el nuevo usuario
								cred = {
									"username": username,
									"password": pw
								}
								db.createUser(cred, username)
								sock.send(b"Usuario creado")
						#Cuando el estado es 0 solo se puede mandar 1 o 2.
						else:
							if status == 0:
								sock.send(b"Opcion invalida")
							
				#Se tiene en cuenta el caso en que el cliente se desconecte		
				except:
					print("Client (%s,%s) is offline"%addr)
					sock.close()
					del socket_status[CONEXIONES.index(sock)]
					CONEXIONES.remove(sock)
					continue
	#Al final del ciclo infinito (por interrupcion del teclado o falla de hardware) se cierra el socket
	server_socket.close()
