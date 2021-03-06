
import socket, select, string, sys
import hashlib, binascii, os

#Este metodo va a permitir una interaccion dinamica con el usuario cada vez que deba ingresar informacion
def prompt():
	sys.stdout.write('<you>')
	sys.stdout.flush()

#Este metodo va a encriptar la contraseña que el usuario ingrese, de tal forma que al enviarse por el socket, si es interceptada, que no sea legible
def hash_password(password):
    #Hash a password for storing.
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

if __name__ == "__main__":
	#Se definen las caracteristicas basicas del socket donde se quiere conectar: Puerto, host, y protocolo (TCP=SOCK_STREAM)
	host = "localhost"
	port = 5000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(3)

	#Se intenta establecer una conexion con el socket servidor
	try:
		s.connect((host, port))
	except:
		print("No se ha podido conectar al servidor")
		sys.exit()

	#La primera parte de la interaccion consiste en elegir un registro o inicio de sesion
	print("Para iniciar sesion escribe 1, para registrarte escribe 2")
	prompt()
	
	#La variable status indica si el cliente debe ingresar usuario(1), contrasenia(2), o no ha elegido (0)
	status = 0
	user = ""
	while True:
		#Se definen los dos sockets, el de la conexion y la entrada por consola para que el usuario envie informacion
		socket_list = [sys.stdin, s]
		read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
		for sock in read_sockets:
			#Este primer socket es el que establece la conexion efectiva con el servidor y recibe la informacion
			if sock == s:
				#Siempre esta a la espera de informacion
				data = sock.recv(4096)
				if not data:
					print ("Desconexion")
					sys.exit()
				else:
					#print("llego respuesta")
					sys.stdout.write(data.decode())
					
					print(status)
					#Caso en que el usuario ya este autorizado
					if(data.decode()=="Ya iniciaste sesion"):
						sys.exit()
					#Caso en que se solicite el usuario
					elif(data.decode()== "Ingresa tu Username: "):
						#Se cambia el estado para enviar el usuario en el formato adecuado
						status = 1
					#Caso en que se solicite la contrasenia
					elif(data.decode()== "Password: "):
						#Se cambia el estado para enviar la contrasenia en el formato adecuado
						status = 2
					#Caso en que el username no corresponda con los de la base de datos
					elif(data.decode()== "Usuario no existe"):
						#Se vuelve al estado inicial
						print("Para iniciar sesion escribe 1, para registrarte escribe 2")
						status = 0
					#Caso en que la contrasenia no  corresponda con la del usuario
					elif(data.decode()== "Credenciales incorrectas"):
						#Se vuelve a solicitar la contrasenia
						print("Password: ")
						status = 2
					#Caso en que la autenticacion fue exitosa
					elif(data.decode()== "Bienvenido"):
						sys.exit()
					#Caso en que la creacion del usuario fue exitosa
					elif(data.decode()== "Usuario creado"):
						sys.exit()
					#Caso en que el usuario que se quiere crear ya exista	
					elif(data.decode()== "Usuario ya existe"):
						#Se vuelve al estado inicial
						print("Para iniciar sesion escribe 1, para registrarte escribe 2")
						status = 0
					prompt()
			#Este es el caso para el socket que envia informacion desde el terminal
			else:
				msg = input()
				res = msg
				
				#Se formatea el envio de los datos de sesion
				if(status == 1):
					res = "user:" + msg
					user = res
				if(status == 2):
					res = "password:" + msg + ":" + user

				s.send(res.encode())
				
				prompt()
