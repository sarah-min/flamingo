import pymongo


# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


print(os.getenv("MY_KEY"))
USER = os.getenv("MY_USERNAME")
PWD = os.getenv("MY_PASSWORD")
    
myclient = pymongo.MongoClient(f"mongodb+srv://{USER}:{PWD}@cluster0.ze8mjac.mongodb.net/")
mydb = myclient["flamingo"]
mycol = mydb["searches"]

mylist = [
  { "id":1 ,"phrase": "slayful", "definition": "you don't know what slay is?"},
]

x = mycol.insert_many(mylist)

#print list of the _id values of the inserted documents:
print(x.__getstate__)

doc = mycol.find_one({"_id": x.inserted_ids[0]})
print(doc["phrase"])



print(x.inserted_ids)