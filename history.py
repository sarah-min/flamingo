# history.py
from pathlib import Path
from dotenv import load_dotenv
import os
import urllib.parse
import certifi
import pymongo
from pymongo.errors import PyMongoError

# load .env from script folder
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

USER = os.getenv("MY_USERNAME")
PWD = os.getenv("MY_PASSWORD")
DBNAME = os.getenv("MY_DB", "flamingo")

if not (USER and PWD):
    raise RuntimeError("Missing MY_USERNAME or MY_PASSWORD in .env")

# URL-encode pwd and use certifi CA bundle
pwd_enc = urllib.parse.quote_plus(PWD)
uri = f"mongodb+srv://{USER}:{pwd_enc}@cluster0.prowd2l.mongodb.net/{DBNAME}?retryWrites=true&w=majority"

try:
    client = pymongo.MongoClient(uri, tls=True, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=10000)
    client.admin.command("ping")
except PyMongoError as e:
    print("MongoDB connection error:", e)
    raise SystemExit(1)

db = client[DBNAME]
col = db["searches"]


mylist = [
    { "phrase": "hi", "definition":"bye"},
    ]

col.insert_many(mylist)

def getHistory():
    for x in col.find():
        # defensive: skip docs missing keys
        phrase = x.get("phrase", "<no phrase>")
        definition = x.get("definition", "<no definition>")
        print(f"{phrase}: {definition}")

def main():
    getHistory()

if __name__ == "__main__":
    main()
