import os
from os.path import dirname, join, abspath
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from models.user import User
from controllers import login
from controllers import index
import pytest
import pymongo
import ssl



    
def reset(): #pragma: no cover
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")  
    db=client["Test"]
    db.Users.delete_one({ "username": "Danzai" })
    db.Users.delete_one({ "username": "Vincent" })
  


@pytest.fixture(autouse=True)
def reset_database(): #pragma: no cover
    reset()

'''
def test_add_user1(reset_database): #pragma: no cover
    
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
    #client = pymongo.MongoClient(config["DB_CONNECTION_STRING"]) 
    db=client["Test"]
    #db.Users.remove({ "username": "Danzai" })
    user_info = login.add_user_to_db("Danzai", "12345", "nyu", "cs", db)


    expected_result = User("2333","Danzai", "nyu", "cs")

    assert user_info.username == expected_result.username, "failed add user test"
'''
   

'''


def test_add_existing_user2():
    
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
    #client = pymongo.MongoClient(config["DB_CONNECTION_STRING"]) 
    db = client["Test"]

    user_info = login.add_user_to_db("Danzai", "12345", "nyu", "cs", db)
    

    expected_result = User("00000","Danzai", "nyu", "cs")

    assert user_info.username == expected_result.username, "failed add existing user test"


'''

def test_add_user3(reset_database): #pragma: no cover
    
    
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
    #client = pymongo.MongoClient(config["DB_CONNECTION_STRING"]) 
    db = client["Test"]
    #db.Users.remove({ "username": "Vincent" })
    user_info = login.add_user_to_db("Vincent", "00000", "Harvard", "econ", db)


    expected_result = User("23333","Vincent", "Harvard", "econ")

    assert user_info.username == expected_result.username, "failed add user 3 test"
   

def test_get_user1(reset_database): #pragma: no cover
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
    #client = pymongo.MongoClient(config["DB_CONNECTION_STRING"]) 
    db=client["Test"]
    #login.add_user_to_db("Vincent2"", "00000", "Harvard", "econ", db)
    get_user = login.get_user_object_in_db("Vincent2", db)

    expected_result = User("00000","Vincent2", "Harvard", "econ")

    assert get_user.school== expected_result.school

    
    
    
    
def test_get_nonexisting_user(): #pragma: no cover
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
    #client = pymongo.MongoClient(config["DB_CONNECTION_STRING"]) 
    db=client["Test"]

    get_user = login.get_user_object_in_db("Tim", db)

    expected_result = None

    assert get_user == expected_result

def test_check_can_login1(): #pragma: no cover

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_login("Danzai","12345",db)

    assert result==True, "Login failed when username and password are correct"


def test_check_can_login2():#pragma: no cover

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_login("Danzai","",db)

    assert result==False, "Login failed when password is empty"


def test_check_can_login3():#pragma: no cover

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_login("","12345",db)

    assert result==False, "Login failed when username is empty"


def test_check_can_login4():#pragma: no cover

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_login("Danzai","78910",db)

    assert result==False, "Login failed when username and password does not match"


def test_can_sign_up1():#pragma: no cover

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_sign_up("Apple", "5678", "nyu", "cs", db)

    assert result==True, "Sign up failed"


def test_can_sign_up2():#pragma: no cover

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_sign_up("Danzai", "12345", "nyu", "cs", db)

    assert result==False, "Sign up failed when user already exist"


def test_can_sign_up3():#pragma: no cover

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_sign_up("Pear", "5678", "", "cs", db)

    assert result==False, "Sign up failed when one of the required field is empty"


