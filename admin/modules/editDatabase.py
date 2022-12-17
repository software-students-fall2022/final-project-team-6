from bson.objectid import ObjectId
import json
from modules.requestCourses import getCourses

def update(db,courseID,display):

    document = db.Courses.find_one({"_id": ObjectId(courseID)})
    if document:
        db.Courses.update_one({'_id':ObjectId(courseID)},{'$set':{'display':display}}) #update the display field to True or False
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'} 

def show(db):
    db.Courses.update_many({},{"$set":{"display":True}})
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}  

def disable(db):
    db.Courses.update_many({},{"$set":{"display":False}})
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}  

def addAllCourses(db,test):
    if test:
        getCourses(db,"UA","CSCI")
    else:
        schoolAbbrs = db.Schools.find({},{ "_id":0, "schoolFullname":0,"image":0, "subjects":0})
        for school in schoolAbbrs:
            schoolAbbr = school["schoolAbbr"]
            docs = db.Schools.find_one({"schoolAbbr":schoolAbbr}, {"_id":0})
            subjects = docs["subjects"]
            for subject in subjects:
                getCourses(db,schoolAbbr,subject["subjectAbbr"])
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}  