import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

import json
import pymongo
import requests
from bson import json_util
from flask import request, Blueprint
from dotenv import dotenv_values
from modules.requestCourses import getCourses
from modules.editDatabase import update,show,disable,addAllCourses
from bson import ObjectId
from .comment import Comment

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

def update_school_subjects(schools, subjects, database):
    i = 10
    for abbr in schools.keys():
        key = {"schoolAbbr": abbr}
        data = {
            "$set":{"schoolFullname": schools[abbr]["name"], "image":"https://picsum.photos/id/" + str(i)+ "/200/150","subjects": []}
           
        }
        if abbr != "NT" and abbr != "ND" and abbr != "US" and abbr != "DC":
            if not database.Schools.find_one(key):
                database.Schools.update_one(key, data, upsert=True)
            i += 1
            schoolDict[abbr] = schools[abbr]["name"]

    for school in subjects.keys():
        for abbr in subjects[school].keys():
            if school in schoolDict.keys():
               
                if (database.Schools.find_one({'schoolAbbr': school, 'subjects': {'$elemMatch': {'subjectAbbr': abbr}}}) == None):
                    database.Schools.update_one({'schoolAbbr': school}, {'$push': {'subjects': {"subjectAbbr":abbr,"subjectFullname":subjects[school][abbr]["name"],"image":"https://picsum.photos/id/" + str(i)+ "/200/150"}}},upsert=True)
                    i += 1
    

@database_page.route('/createSchool')
def createSchoolsCollection():
    schoolsAPI = requests.get(url+"schools")
    schoolsAPI.encoding = 'utf-8'
    schools  = json.loads(str(schoolsAPI.text))

    subjectsAPI = requests.get(url+"subjects")
    subjectsAPI.encoding = 'utf-8'
    subjects  = json.loads(str(subjectsAPI.text))
    
    update_school_subjects(schools, subjects, db)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}  

def get_course_info_by_course_id(course_id, database):
    print("course id: " + course_id)
    course_info = database.Courses.find_one({"_id": ObjectId(course_id)})
    if(course_info == None):
        return None
    course_info = json_util.loads(json_util.dumps(course_info))
    return course_info

def get_course_comments(course_id, database):
    course_comments = database.Comments.find_one({"course_id": ObjectId(course_id)})
    if(course_comments == None):
        return []
    comments = course_comments["comments"]
    comments_list = []
    if(comments != None):
        for comment in comments:
            comments_list.append(Comment(username = comment["username"], comment = comment["comment"], rating = int(comment["rating"]), comment_id=str(comment["comment_id"])))
    return comments_list

def calculate_overall_ratings(comments_list):
    if(len(comments_list) == 0):
        return -1
    total = 0
    for comment in comments_list:
        total += comment.rating
    return round(total / len(comments_list),1)

def update_overall_rating(course_id, database):
    comments_list = get_course_comments(course_id, database)
    ratings = calculate_overall_ratings(comments_list)
    if database.Comments.find_one({"course_id": ObjectId(course_id)}) == None:
       return -1
    database.Comments.update_one({"course_id": ObjectId(course_id)}, {"$set": {"overall_rating": ratings}})
    database.Courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"overallRating": ratings}})
    return 0

def delete_course_comment(course_id, comment_id, database):
    course_comments = database.Comments.find_one({"course_id": ObjectId(course_id)})
    if(course_comments == None):
        return False
    
    comments = course_comments["comments"]
   
    if(comments != None):
        for comment in comments:
            if(str(comment["comment_id"]) == comment_id):
                comments.remove(comment)
                database.Comments.update_one({"course_id": ObjectId(course_id)}, {'$set': {"comments": comments}})
                update_overall_rating(course_id, database)
                return True
    return False