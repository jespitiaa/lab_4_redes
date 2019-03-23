import pymongo

uri = 'mongodb://admin:admin1@ds121026.mlab.com:21026/redes_auth_tcp'
client=pymongo.MongoClient(uri)
db = client.get_database["redes_auth_tcp"]
users_collection=db.users
def getUser(pUsername):
    user=users_collection.find_one({"username":pUsername})
	return user
def createUser(json):
    succes=false
    if users_collection.find_one({"username":pUsername}) is None:
	   users_collection.insert_one(json)
       succes=true
	return succes
def deleteUser (pUsername):
    if users_collection.find_one({"username":pUsername}) is None:
        return false
    else:
        users_collection.deleteOne({"username": pUsername})
        return true;	       
