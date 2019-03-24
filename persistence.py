
import pymongo
import sys
import pprint
import hashlib, binascii, os


uri = 'mongodb://admin:admin1@ds121026.mlab.com:21026/redes_auth_tcp'
client=pymongo.MongoClient(uri)
db = client.get_default_database()
users_collection=db.users
def getUsers():
	usuarios=users_collection.find({})
	for u in usuarios:
		pprint.pprint(u)
	return usuarios
def getUser(pUsername):
	user=users_collection.find_one({"username":pUsername})
	return user
def createUser(json, pUsername):
	succes=False
	if users_collection.find_one({"username":pUsername}) == None:
		succes=True, users_collection.insert_one(json)
		return succes
def deleteUser (pUsername):
	if users_collection.find_one({"username":pUsername}) == None:
		return False
	else:
		users_collection.delete_one({"username": pUsername})
		return True;


def hash_password(password):
    #Hash a password for storing.
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
		#Verify a stored password against one provided by user
		salt = stored_password[:64]
		stored_password = stored_password[64:]
		pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),salt.encode('ascii'), 100000)
		pwdhash = binascii.hexlify(pwdhash).decode('ascii')
		return pwdhash == stored_password
	

def main(args):
	print("get by username")
	print(getUser("satiagoRM"))
	print("get users")
	print(getUsers())
	print("usuario a insertar: {'username': 'prueba', 'password': 'juancjo12'}")
	print(createUser({'username': 'prueba', 'password': 'juancjo12'}, "prueba"))
	print("confirmacion")
	print(type(getUser("prueba") ))
	print("preuba de borrar usuario prueba")
	print(deleteUser("prueba"))
	print(getUsers())
	client.close()
	hashed = hash_password("hola")
	print("pw : hola, hash : " + hashed)
	print("normal vs hashed: " + str(verify_password(hashed, "hola")))
	print("hashed vs hashed: " + str(verify_password(hashed, hashed)))
if __name__ == '__main__':
	main(sys.argv[1:])
