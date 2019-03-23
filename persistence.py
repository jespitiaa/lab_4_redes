import pymongo
import sys
import pprint

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
    if users_collection.find_one({"username":pUsername}) is None:
        succes=True, users_collection.insert_one(json)
	return succes
def deleteUser (pUsername):
    if users_collection.find_one({"username":pUsername}) is None:
        return False
    else:
        users_collection.delete_one({"username": pUsername})
        return True;

def main(args):
    print("get by username")
    print(getUser("satiagoRM"))
    print("get users")
    print(getUsers())
    print("usuario a insertar: {'username': 'prueba', 'password': 'juancjo12'}")
    print(createUser({'username': 'prueba', 'password': 'juancjo12'}, "prueba"))
    print("confirmacion")
    print(getUser("prueba"))
    print("preuba de borrar usuario prueba")
    print(deleteUser("prueba"))
    print(getUsers())
    client.close()
if __name__ == '__main__':
    main(sys.argv[1:])
