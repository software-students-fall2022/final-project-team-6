import pymongo
from dotenv import dotenv_values

config = dotenv_values(".env")

client = pymongo.MongoClient(config["DB_CONNECTION_STRING"])   
db=client[config["DB_NAME"]]