import os
from os.path import dirname, join, abspath
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from models import database
import pytest
import pymongo


'''
def test_add_schools_data():
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")  
    db=client["Test_DB"]
    doc1 = {
            "schoolAbbr": "UA", 
            "schoolFullname": "College of Arts and Science",
            "subjects": "Computer Science"
        }
    db.Schools.insert_one(doc1) # insert a new document
    doc2 = {
            "schoolAbbr": "UF", 
            "schoolFullname": "Liberal Studies",
            "subjects": "Political Science"
        }
    db.Schools.insert_one(doc2) # insert a new document
    doc3 = {
            "schoolAbbr": "SHU", 
            "schoolFullname": "NYU Shanghai",
            "subjects": "Data Science"
        }
    db.Schools.insert_one(doc3) # insert a new document
'''
'''
def test_delete_schools_data():
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")  
    db=client["Test_DB"]
    db.Schools.delete_one({ "schoolAbbr": "UA" })
    db.Schools.delete_one({ "schoolAbbr": "UF" })
    db.Schools.delete_one({ "schoolAbbr": "SHU" })
'''
'''
def test_add_courses_data():
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")  
    db=client["Test_DB"]
    doc1 = {
            "courseName": "Software Engineering",
            "subjectFullname": "Computer Science", 
            "schoolFullname": "College of Arts and Science",
        }
    db.Courses.insert_one(doc1) # insert a new document
    doc2 = {
            "courseName": "Operating System",
            "subjectFullname": "Computer Science", 
            "schoolFullname": "College of Arts and Science",
        }
    db.Courses.insert_one(doc2) # insert a new document
    doc3 = {
            "courseName": "DMA",
            "subjectFullname": "Computer Science", 
            "schoolFullname": "College of Arts and Science",
        }
    db.Courses.insert_one(doc3) # insert a new document
'''
'''
def test_delete_course_data():
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")  
    db=client["Test_DB"]
    db.Courses.delete_one({ "courseName": "Software Engineering" })
    db.Courses.delete_one({ "courseName": "Operating System" })
    db.Courses.delete_one({ "courseName": "DMA" })
'''
'''
def test_add_comment_data():
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")  
    db=client["Test_DB"]
    doc1 = {
            "username": "hello",
            "comment": "This is a good class.", 
            "rating": 2.0 
        }
    db.Comments.insert_one(doc1) # insert a new document
    doc2 = {
            "username": "hello2",
            "comment": "This is a bad class.", 
            "rating": 1.0
        }
    db.Comments.insert_one(doc2) # insert a new document
    doc3 = {
            "username": "hello3",
            "comment": "This is a okay class.", 
            "rating": 1.5 
        }
    db.Comments.insert_one(doc3) # insert a new document
'''
'''
def test_delete_comment_data():
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")  
    db=client["Test_DB"]
    db.Comments.delete_one({ "username": "hello" })
    db.Comments.delete_one({ "username": "hello2" })
    db.Comments.delete_one({ "username": "hello3" })
'''
'''
def test_fetch_all_subjects():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")  
    
    db=client["Test_DB"]
    
    output=database.fetch_all_subjects(db)
    
    expected_result = ["Computer Science", "Political Science", "Data Science"]
    
    check=True
    
    for i in range (len(output)):
        
        if output[i]==expected_result[i]:
            
            pass
        
        else:
            
            check=False

    assert check==True, "failed to get all subjects"
'''
def test_get_course_info_by_course_id():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")  
    
    db=client["Test_DB"]

    output=database.get_course_info_by_course_id("63992e3240e7461f5b55999a", db)

    expected_result="Software Engineering"

    assert output['courseName']==expected_result, "failed to get course info by course id"

def test_get_course_info_by_course_id2():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")  
    
    db=client["Test_DB"]

    expected_result=None

    try:

        output=database.get_course_info_by_course_id("63992e3240e7461f5b55999poiu", db)

    except:    

        output=None

    assert output==expected_result, "failed to get course info by course id when course does not exist"


def test_fetch_all_schools(): #pragma: no cover
    
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
    #client = pymongo.MongoClient(config["DB_CONNECTION_STRING"]) 
    db=client["Test_DB"]
    #db.Users.remove({ "username": "Danzai" })
    school_info = database.fetch_all_schools(db)

    expected_result = ["College of Arts and Science", "Liberal Studies", "NYU Shanghai"]

    check = True
    
    for i in range(0,len(school_info)):
        
        if expected_result[i] != school_info[i]:

            check = False

    assert check == True, "fail to get school full names"



def test_get_all_courses_by_school_subject_fullname(): #pragma: no cover
    
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
  
    db=client["Test_DB"]

    course_info = database.get_all_courses_by_school_subject_fullname("College of Arts and Science", "Computer Science", db)

    expected_result = ["Software Engineering", "Operating System", "DMA"]

    check = True
    
    for i in range(0,len(course_info)):
        
        if expected_result[i] != course_info[i]["courseName"]:

            check = False

    assert check == True, "fail to get course info"


            
def test_get_all_courses_by_school_subject_fullname2(): #pragma: no cover
    
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
  
    db=client["Test_DB"]

    course_info = database.get_all_courses_by_school_subject_fullname("College of Arts and Science", "Film", db)

    expected_result = []
    '''
    check = True
    
    for i in range(0,len(course_info)):
        
        if expected_result[i] != course_info[i]["courseName"]:

            check = False
    '''

    assert course_info == expected_result, "fail to get course info"

