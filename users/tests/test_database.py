import os
from os.path import dirname, join, abspath
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from models import database
import pytest
import pymongo
from bson import ObjectId

def test_get_course_info_by_course_id():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")  
    
    db=client["Test_DB"]

    output=database.get_course_info_by_course_id("639aa34c9cbb8d66ffcf1a35", db)

    expected_result="Quantitative Reasoning: Prob,Stats & Decisn-Mkng 001"

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
    
    for i in range(0,len(expected_result)):
        
        if expected_result[i] not in school_info:

            check = False

    assert check == True, "fail to get school full names"



def test_get_all_courses_by_school_subject_fullname(): #pragma: no cover
    
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
  
    db=client["Test_DB"]

    course_info = database.get_all_courses_by_school_subject_fullname("College of Arts and Science", "Computer Science", db)

    expected_result = ["Quantitative Reasoning: Prob,Stats & Decisn-Mkng 001", "Life Science: Earth, Life & Time 001", "Physical Science: Energy & The Environment 010"]

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

    assert course_info == expected_result, "fail to get course info"


def test_get_course_comments():
    
    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
  
    db=client["Test_DB"]

    course_comments = database.get_course_comments("6397d5499cbb8d66ff9ade0f",db)

    real_comment=[]

    for i in range (len(course_comments)):

        real_comment.append(course_comments[i].comment)

    expected_result = ["I love this class", "waeewa","eee"]

    check = True

    for i in range(0,len(expected_result)):

        if expected_result[i] not in real_comment:
            
            check = False

    assert check == True, "fail to get comments"


def test_update_overall_rating():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
  
    db=client["Test_DB"]

    course_id = "6397d5499cbb8d66ff9ade0f"

    update_rating = database.update_overall_rating("6397d5499cbb8d66ff9ade0f", db)

    rating = db.Comments.find_one({"course_id": ObjectId(course_id)})
    
    expected_value = 4.7

    assert rating["overall_rating"]== expected_value, "fail to test overall rating"


def test_search():

        client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
  
        db=client["Test_DB"]

        course_list = database.search("Life Science: Earth, Life & Time 001", db)

        expected_value = "College Core Curriculum"

        assert course_list[0]["subjectFullname"] == "College Core Curriculum", "fail to search for the course"


def test_calculate_overall_ratings():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
  
    db=client["Test_DB"]

    comments_list=database.get_course_comments("6397d5499cbb8d66ff9ade0f",db)

    result=database.calculate_overall_ratings(comments_list)

    expected_result=4.7

    assert result==expected_result, "fail to calculate overall ratings"


def test_add_comment():

    client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")
  
    db=client["Test_DB"]

    database.add_comment("6397d5c09cbb8d66ff9ae84c", "hello4", "I love this class", 5, db)

    comment_list=database.get_course_comments("6397d5c09cbb8d66ff9ae84c", db)

    real_comment=[]

    for i in range (len(comment_list)):

        real_comment.append(comment_list[i].comment)

    check=True

    target="I love this class"

    if target not in real_comment:

        check=False
    
    assert check==True, "Failed to add comment"


    
