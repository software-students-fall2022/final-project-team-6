import sys
from os.path import dirname, join, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

import json

from flask.testing import FlaskClient
from app import app

page_url = '/database'

import json
import pymongo
from dotenv import dotenv_values
from modules.updateDisplay import update


client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")   
db=client["Test_DB"]

class Tests:
    def test_addAll(self):
        pass
    
    def test_displayAlltrue(self):
        response = app.test_client().get('/database/displayAlltrue')
        assert response.status_code == 200
        assert response.data == json.dumps({'success':True}).encode("utf-8")

    def test_displayAllfalse(self):
        response = app.test_client().get('/database/displayAllfalse')
        assert response.status_code == 200
        assert response.data == json.dumps({'success':True}).encode("utf-8")

    def test_displayUpdate_true(self):
        response = update(db,"63992e3240e7461f5b55999a",True)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})

    def test_displayUpdate_false(self):
        response = update(db,"63992e3240e7461f5b55999a",False)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})

    def test_createSchoolsCollection(self):
        response = app.test_client().get('/database/createSchool')
        assert response.status_code == 200
        assert response.data == json.dumps({'success':True}).encode("utf-8")