import os
from os.path import dirname, join, abspath
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from models import database
import pytest
import pymongo


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