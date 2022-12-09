import os
from os.path import dirname, join, abspath
import sys
from models.user import User

sys.path.append(dirname(dirname(abspath(__file__))))

from controllers import index
from controllers import login

import pymongo


def test_check_can_login1():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_login("Danzai","12345",db)

    assert result==True, "Login failed when username and password are correct"


def test_check_can_login2():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_login("Danzai","",db)

    assert result==False, "Login failed when password is empty"


def test_check_can_login3():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_login("","12345",db)

    assert result==False, "Login failed when username is empty"


def test_check_can_login4():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_login("Danzai","78910",db)

    assert result==False, "Login failed when username and password does not match"


def test_can_sign_up1():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_sign_up("Apple", "5678", "nyu", "cs", db)

    assert result==True, "Sign up failed"


def test_can_sign_up2():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_sign_up("Danzai", "12345", "nyu", "cs", db)

    assert result==False, "Sign up failed when user already exist"


def test_can_sign_up3():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")

    db = client["Users_Test"]

    result=login.check_can_sign_up("Pear", "5678", "", "cs", db)

    assert result==False, "Sign up failed when one of the required field is empty"


