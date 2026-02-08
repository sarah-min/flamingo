from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from pathlib import Path

load_dotenv()

import pymongo

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

USER = os.getenv("MY_USERNAME")
PWD = os.getenv("MY_PASSWORD")
    
myclient = pymongo.MongoClient(f"mongodb+srv://{USER}:{PWD}@cluster0.ze8mjac.mongodb.net/")
mydb = myclient["flamingo"]
mycol = mydb["searches"]


def getHistory():
    for x in mycol.find(): 
        print(x["phrase"] + ": " + x["definition"])



def main():
    getHistory()

main()


