import socket, select

print("joekd")
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
		pwdhash = hashlib.pbkdf2_hmac('sha512', 
									  provided_password.encode('utf-8'), 
									  salt.encode('ascii'), 
									  100000)
		pwdhash = binascii.hexlify(pwdhash).decode('ascii')
		return pwdhash == stored_password
	
	
	def broadcast(sock,msg):
		for s in CONEXIONES:
			if(s==sock):
				continue
			sock.send(msg)
	
	while True:
		read_sockets, write_sockets, error_sockets = select.select(CONEXIONES, [], [])
		
		for sock in read_sockets:
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				CONEXIONES.append(sockfd)
				print("El cliente (%s, %s) está conectado" %addr)

			else:
				try:
					data = sock.recv(BUFFER)
					if data:
						sock.send(data)
						print(data.decode())
				except:
					print("Client (%s,%s) is offline"%addr)
					sock.close()
					CONEXIONES.remove(sock)
					continue
	server_socket.close()