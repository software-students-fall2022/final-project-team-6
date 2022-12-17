import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

import json
import pymongo
import requests

from flask import request, Blueprint
from dotenv import dotenv_values
from modules.requestCourses import getCourses
from modules.database import update,show,disable,addAllCourses


config = dotenv_values(".env")
database_page = Blueprint("database_page", __name__ )


client = pymongo.MongoClient(config["DB_CONNECTION_STRING"])   
db=client[config["DB_NAME"]]

url = 'https://schedge.a1liu.com/'

schoolDict = {}

@database_page.route('/addAll')
def addAll():
    return addAllCourses(db,test = False)

@database_page.route('/displayAlltrue')
def displayAlltrue():
    return show(db)

@database_page.route('/displayAllfalse')
def displayAllfalse():
    return disable(db)

@database_page.route('/update', methods=['POST'])
def displayUpdate():
    return update(db,    courseID = request.form.get('courseID'),    display = str(request.form.get('display')))
    #db.Courses.update_one({'_id':ObjectId(courseID)},{'$set':{'display':display}}) #update the display field to True or False
    

@database_page.route('/createSchool')
def createSchoolsCollection():
    schoolsAPI = requests.get(url+"schools")
    schoolsAPI.encoding = 'utf-8'
    schools  = json.loads(str(schoolsAPI.text))

    subjectsAPI = requests.get(url+"subjects")
    subjectsAPI.encoding = 'utf-8'
    subjects  = json.loads(str(subjectsAPI.text))

    i = 10
    for abbr in schools.keys():
        key = {"schoolAbbr": abbr}
        data = {
            "$set":{"schoolFullname": schools[abbr]["name"], "image":"https://picsum.photos/id/" + str(i)+ "/200/150"}
        }
        if abbr != "NT" and abbr != "ND" and abbr != "US" and abbr != "DC":
            
            db.Schools.update_one(key, data, upsert=True)
            i += 1
            schoolDict[abbr] = schools[abbr]["name"]

    for school in subjects.keys():
        for abbr in subjects[school].keys():
            if school in schoolDict.keys():
                db.Schools.update_one({'schoolAbbr': school}, {'$push': {'subjects': {"subjectAbbr":abbr,"subjectFullname":subjects[school][abbr]["name"],"image":"https://picsum.photos/id/" + str(i)+ "/200/150"}}},upsert=True)
                i += 1
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}  
