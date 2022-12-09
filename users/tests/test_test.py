import os
from os.path import dirname, join, abspath
import sys

sys.path.append(dirname(dirname(abspath(__file__))))
from models.user import User
from controllers import login
from controllers import index
import pymongo
import ssl



def test_add_user1():
    
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
    #client = pymongo.MongoClient(config["DB_CONNECTION_STRING"]) 
    db=client["Test"]
    #db.Users.remove({ "username": "Danzai" })
    user_info = login.add_user_to_db("Danzai", "12345", "nyu", "cs", db)


    expected_result = User("2333","Danzai", "nyu", "cs")

    assert user_info.username == expected_result.username, "failed add user test"

'''
def test_add_existing_user2():
    
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
    #client = pymongo.MongoClient(config["DB_CONNECTION_STRING"]) 
    db = client["Test"]

    user_info = login.add_user_to_db("Danzai", "12345", "nyu", "cs", db)
    

    expected_result = User("00000","Danzai", "nyu", "cs")

    assert user_info.username == expected_result.username, "failed add existing user test"

'''
def test_add_user3():
    
    
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
    #client = pymongo.MongoClient(config["DB_CONNECTION_STRING"]) 
    db = client["Test"]
    #db.Users.remove({ "username": "Vincent" })
    user_info = login.add_user_to_db("Vincent", "00000", "Harvard", "econ", db)


    expected_result = User(user_info._id.str,"Vincent", "Harvard", "econ")

    assert user_info.username == expected_result.username, "failed add user 3 test"


def test_get_user1():
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
    #client = pymongo.MongoClient(config["DB_CONNECTION_STRING"]) 
    db=client["Test"]

    get_user = login.get_user_object_in_db("Vincent", db)

    expected_result = User(get_user._id.str,"Vincent", "Harvard", "econ")

    assert get_user.school== expected_result.school
    
def test_get_nonexisting_user():
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
    #client = pymongo.MongoClient(config["DB_CONNECTION_STRING"]) 
    db=client["Test"]

    get_user = login.get_user_object_in_db("Tim", db)

    expected_result = None

    assert get_user == expected_result
