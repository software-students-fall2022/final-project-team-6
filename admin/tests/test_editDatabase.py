from bson.objectid import ObjectId
import json
import pymongo
from modules.requestCourses import getCourses
from modules.editDatabase import update,show,disable,addAllCourses

client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")   
db=client["Test"]
courseID = ""
class Tests:

    def test_update(self):
        response = update(db, "639d0ad69cbb8d66ff07f51f", True)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})
    
    def test_update_false(self):
        response = update(db, "639d0ed65cbb8d66ff07f50f", True)
        assert response == ('{"success": false}', 400, {'ContentType': 'application/json'})

    def test_show(self):
        response = show(db)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})

    def test_disable(self):
        response = disable(db)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})

    def test_addAllCourses(self):
        response = addAllCourses(db, True)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})