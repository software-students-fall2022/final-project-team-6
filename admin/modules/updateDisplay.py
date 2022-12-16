from bson.objectid import ObjectId
import json

def update(db,courseID,display):

    document = db.Courses.find_one({"_id": ObjectId(courseID)})
    if document:
        db.Courses.update_one({'_id':ObjectId(courseID)},{'$set':{'display':display}}) #update the display field to True or False
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'} 

