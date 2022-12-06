import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, Blueprint, redirect, url_for, make_response, session, flash
import face_recognition
import os
import matplotlib.pyplot as plt 
from PIL import Image, ImageDraw
from io import BytesIO
import base64
import re
from hsemotion.facial_emotions import HSEmotionRecognizer
from numpy import asarray
import datetime

def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )

index_page = Blueprint( "index_page", __name__ )
app = Flask(__name__)
app.secret_key = "secret key"

if(is_docker()):
    client = pymongo.MongoClient("db", 27017)
else:
    client = pymongo.MongoClient("127.0.0.1", 27017)
   
   
db=client["Team6"]


@index_page.route('/')
def home():
    return render_template('/photo/main_page.html')

@index_page.route('/back', methods=['GET'])
def back():
    return redirect(url_for("index_page.home"))

def face_detect(image_bytes):
    image = None
    try:
        image = face_recognition.load_image_file(image_bytes)
    except:
        return None
    
    
    face_locations = face_recognition.face_locations(image,1,"cnn") 
    result = []
    imgs = []
    #test code, can be removed
  
    for face_location in face_locations:
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
        face_image = image[top:bottom, left:right]
        imgs.append(Image.fromarray(face_image))
       
   
    if(len(imgs) > 0):
        for img in imgs:
            buffer = BytesIO()
            img.save(buffer,format="PNG")                  
            myimage = buffer.getvalue()   
            myimage = "data:image/png;base64," + base64.b64encode(myimage).decode('utf-8')
            result.append(myimage)
        
        
    return result
   

def get_emotion(image_bytes):
  model_name='enet_b0_8_best_afew'
  fer=HSEmotionRecognizer(model_name=model_name,device='cpu')
  
  img = Image.open(image_bytes).convert('RGB')
  numpydata = asarray(img)
   
  emotion,scores=fer.predict_emotions(numpydata,logits=True)
  return emotion
  

def face_detect_with_emotions(image_bytes):
    imgs = face_detect(image_bytes)   
    result = []
    
    if(imgs is not None and len(imgs) > 0):
        for img in imgs:
            raw = re.sub('^data:image/.+;base64,', '', img)
            raw = BytesIO(base64.b64decode(raw))
            emotion = get_emotion(raw)
            result.append({"img":img,"emotion":emotion})
        return result
    else:
        return None


@index_page.route('/upload', methods=['POST'])
def upload():
    
    photo = request.form.get('photo') #SAVE THIS TO DATABASE (ORIGINAL PHOTO)
   
    if(photo == None):
        return render_template('/photo/result_page.html', results=None)
    
    raw_image = re.sub('^data:image/.+;base64,', '', photo)
    image_bytes = BytesIO(base64.b64decode(raw_image))
    
    results = face_detect_with_emotions(image_bytes)
    
    if(results is not None):
        doc = {
            "original": photo,
            "results": results,
            "created_at": datetime.datetime.utcnow()
        }
        db.Image.insert_one(doc)
        return render_template('/photo/result_page.html', results=results)
    else:
        return render_template('/photo/result_page.html', results=None)
        