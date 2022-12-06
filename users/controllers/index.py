import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, Blueprint, redirect, url_for, make_response, session, flash
import datetime
import os
import sys

index_page = Blueprint( "index_page", __name__ )

app = Flask(__name__)
app.secret_key = "secret key"

def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )
if(is_docker()):
    client = pymongo.MongoClient("db", 27017)
else:
    client = pymongo.MongoClient("mongodb+srv://okkiris:F3iQz3hSCxOwhhOu@cluster0.ubegai3.mongodb.net/?retryWrites=true&w=majority")
    

db=client["Team6"]

def analyze(collection):

    emotion_dict={
        'Anger':0,
        'Contempt':1,
        'Disgust':2,
        'Fear':3,
        'Happiness':4,
        'Neutral':5,
        'Sadness':6,
        'Surprise':7
    }
    
    docs = collection.find({}).sort("created_at", -1)
   
    
    output = []
    
    total=0

    count_array=[0,0,0,0,0,0,0,0]

    for doc in docs:
        
        for result in doc['results']:

            total += 1
                
            emotion = emotion_dict[result['emotion']]

            count_array[emotion] += 1


    output=[0,0,0,0,0,0,0,0]

    for c in range(len(count_array)):

        output[c]=count_array[c]/total
    
    #print(output)

    key_list = list(emotion_dict.keys())

    val_list = list(emotion_dict.values())

    output_dict={}

    for n in range(len(output)):

        position = val_list.index(n)

        output_dict[key_list[position]]=output[n]
    
    #print(output_dict)

    maxPercentage = max(output)

    minPercentage = min(output)

    maxEmotion = []

    minEmotion = []
    
    #print(minPercentage)

    #print(maxPercentage)

    for key in output_dict.keys():

        if output_dict[key] == maxPercentage:
            
            key = key + " "

            maxEmotion.append(key)
            
            #print(key)
    
    for key in output_dict.keys():

        if output_dict[key] == minPercentage:

            key = key + " "

            minEmotion.append(key)


    output_dict["MAX"] = "".join(maxEmotion)
    
    output_dict["MIN"] = "".join(minEmotion)

    return output_dict


def compute_percentage(collection):

    emotion_dict={
        'Anger':0,
        'Contempt':1,
        'Disgust':2,
        'Fear':3,
        'Happiness':4,
        'Neutral':5,
        'Sadness':6,
        'Surprise':7
    }
    
    docs = collection.find({}).sort("created_at", -1)
   
    
    output = []
    
    
    for doc in docs:
        
        docs_id=doc['_id']

        total=0

        count_array=[0,0,0,0,0,0,0,0]

        for result in doc['results']:

            total+=1
                
            emotion=emotion_dict[result['emotion']]

            count_array[emotion]+=1

        output=[0,0,0,0,0,0,0,0]

        for c in range(len(count_array)):

            output[c]=count_array[c]/total

        key_list = list(emotion_dict.keys())

        val_list = list(emotion_dict.values())

        output_dict={}

        for n in range(len(output)):

            position = val_list.index(n)

            output_dict[key_list[position]]=output[n]

        collection.update_one({"_id" :ObjectId(docs_id)},{"$set":{"Percentage":output_dict}})
    return output

def find_max(collection):

    docs = collection.find({}).sort("created_at", -1)
    emotion_dict={
        'Anger':0,
        'Contempt':1,
        'Disgust':2,
        'Fear':3,
        'Happiness':4,
        'Neutral':5,
        'Sadness':6,
        'Surprise':7
    }

    output = []

    for doc in docs:

        docs_id=doc['_id']

        count_array=[0,0,0,0,0,0,0,0]
        output=[]

        for result in doc['results']:
            
            emotion=emotion_dict[result['emotion']]

            count_array[emotion]+=1

        max = 0
        for c in range(len(count_array)):
            if (count_array[c] > max):
                max = count_array[c]


        for i in range(len(count_array)):
            if (count_array[i] == max):
                output.append(i)
        
        key_list = list(emotion_dict.keys())
        val_list = list(emotion_dict.values())


        for j in range(len(output)):
            position = val_list.index(output[j])
            output[j] = key_list[position]

    
        
        collection.update_one({"_id" :ObjectId(docs_id)},{"$set":{"MaxEmotion":output}})
    return output

def find_min(collection):

    emotion_dict={
        'Anger':0,
        'Contempt':1,
        'Disgust':2,
        'Fear':3,
        'Happiness':4,
        'Neutral':5,
        'Sadness':6,
        'Surprise':7
    }
    
    
    docs = collection.find({}).sort("created_at", -1)
    output = []


    for doc in docs:

        docs_id=doc['_id']

        count_array=[0,0,0,0,0,0,0,0]
        output=[]

        for result in doc['results']:
            
            emotion=emotion_dict[result['emotion']]

            count_array[emotion]+=1

        min = sys.maxsize
        for c in range(len(count_array)):
            if (count_array[c] < min and count_array[c] > 0):
                min = count_array[c]

        for i in range(len(count_array)):
            if (count_array[i] == min):
                output.append(i)

        key_list = list(emotion_dict.keys())
        val_list = list(emotion_dict.values())


        for j in range(len(output)):
            position = val_list.index(output[j])
            output[j] = key_list[position]
                
      
        
        collection.update_one({"_id" :ObjectId(docs_id)},{"$set":{"MinEmotion":output}})
    return output


@index_page.route('/photo_page', methods=['POST'])
def photo_page():
    id = request.form.get('id')
    #remove the last / from the id
    id = id[:-1]
    doc = db['Image'].find_one({"_id": ObjectId(id)})
    return render_template('/photo/details.html', doc= doc)
   
@index_page.route('/')
def home():
    collection = db.Image
    info=analyze(collection)
    compute_percentage(collection)
    find_max(collection)
    find_min(collection)

    docs = db.Image.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp

    return render_template('/photo/index.html', docs = docs, analysis = info)

@index_page.route('/delete', methods=['POST'])
def delete():
    id = request.form.get('id')
    #remove the last / from the id
    id = id[:-1]
    db['Image'].delete_one({"_id": ObjectId(id)})
    
    return redirect('/')

'''
    doc = {
            "original": 'photo',
            "results": [{"img":'img',"emotion":'Anger'},{"img":'img',"emotion":'Contempt'},{"img":'img',"emotion":'Disgust'},
            {"img":'img',"emotion":'Fear'},{"img":'img',"emotion":'Happiness'},{"img":'img',"emotion":'Neutral'},{"img":'img',"emotion":'Sadness'},
            {"img":'img',"emotion":'Happiness'},{"img":'img',"emotion":'Surprise'}]
        }

    db.TestImage.insert_one(doc)

    doc = {
            "original": 'photo',
            "results": [{"img":'img',"emotion":'Anger'},{"img":'img',"emotion":'Neutral'},
            {"img":'img',"emotion":'Fear'}, {"img":'img',"emotion":'Neutral'},{"img":'img',"emotion":'Sadness'}]
        }

    db.TestImage.insert_one(doc)
'''

    #return render_template('/photo/photo_demo.html')

@index_page.route("/details")
def gallery():
    return render_template('/photo/details.html')

'''
@index_page.route('/upload', methods=['POST'])
def upload():
    photo = request.form.get('photo')
    #machine learning stuff here
    #save image to Mongodb

    doc = {
            "Image": photo,
            "created_at": datetime.datetime.utcnow()
    }
    db.Image.insert_one(doc) # insert a new document
    docs = db.Image.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp

    return render_template('/photo/photo_response_demo.html', imgBase64 = photo)
'''
