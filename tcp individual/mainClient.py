import socket, select, string, sys

def prompt():
	sys.stdout.write('<you>')
	sys.stdout.flush()

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
	
if __name__ == "__main__":
		
	host = localhost
	port = 5000
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(3)
	
	try:
		s.connect((host, port))
	except:
		print("No se ha podido conectar al servidor")
		sys.exit()
	
	print("Conectado al servidor" + hash_password("hola"))