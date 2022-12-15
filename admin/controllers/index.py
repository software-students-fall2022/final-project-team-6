import pymongo
from flask import Flask, render_template, request, Blueprint, redirect, url_for, make_response, session, flash
from dotenv import dotenv_values
from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))
from models.requestCourses import getCourses

config = dotenv_values(".env")

index_page = Blueprint("index_page", __name__ )
app = Flask(__name__)
app.secret_key = "secret key"

client = pymongo.MongoClient(config["DB_CONNECTION_STRING"])   
db=client[config["DB_NAME"]]

url = 'https://schedge.a1liu.com/'

@index_page.route('/')
def school():
    #only demonstrate school name 
    docs = db.Schools.find({},{ "_id":0,  "subjects":0})
    docs = db.Schools.find({},{ "_id":0,  "subjects":0})
    return render_template('/courses/schools.html',docs=docs)

@index_page.route('/subjects',methods = ["GET"])
def subject():
    school = request.args.get('schoolAbbr').upper()
    docs = db.Schools.find_one({"schoolAbbr":school}, {"_id":0})
    docs = docs["subjects"]
    return render_template('/courses/subjects.html',docs=docs,schoolAbbr = school)

#query should be like "http://127.0.0.1:5000/courses?schoolAbbr=UA&subjectAbbr=CSCI"
@index_page.route('/courses', methods=['GET'])
def course():
    schoolAbbr = request.args.get("schoolAbbr").upper()
    subjectAbbr = request.args.get("subjectAbbr").upper()

    docs = getCourses(db,schoolAbbr,subjectAbbr)

    return render_template('/courses/courses.html',docs=docs)



"""
Left here for reference
Original Schema:
{
    "name":"Realtime and Big Data Analytics",
    "deptCourseId":"2436",
    "subjectCode":
    {
        "code":"CSCI",
        "school":"GA"
    },
    "sections":
    [
        {
            "registrationNumber":3539,
            "code":"001",
            "instructors":
            [
                "Yang Tang"
            ],
            "type":"Lecture",
            "status":"Closed",
            "meetings":
            [
                {
                    "beginDate":"2021-09-02 19:10:00",
                    "minutesDuration":110,
                    "endDate":"2021-12-14 23:59:00"
                }
            ],
            "instructionMode":"In-Person",
            "name":"Realtime and Big Data Analytics",
            "minUnits":0.0,
            "maxUnits":3.0,
            "location":"GCASL - Room: 461"
        }
    ]
}
Target Schema:
{
    "courseName" : "Ethics",
    "deptCourseId" : "40",
    "subjectAbbr" : "PHIL",
    "schoolAbbr" : "UA",
   "registrationNumber" : 23262.0,
    "code" : "001",
    "instructors" : "Sanford Laurence Diehl",
    "type" : "Lecture",
    "status" : "Open",
    "instructionMode" : "In-Person",
    "units" : 4.0,
    "location" : "Meyer Hall - Room: 122",
    "display" : False,
    "url" : "https://www.ratemyprofessors.com/search/teachers?query=Sanford%20Laurence%20Diehl&sid=U2Nob29sLTY3NQ=="
    "id" : '6397d5499cbb8d66ff9ade0f'，
    "overallRating" : 1
}
"""