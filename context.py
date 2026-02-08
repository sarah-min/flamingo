from pathlib import Path
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import pymongo
import certifi
import urllib.parse
from pymongo.errors import PyMongoError
 
 # load .env from script folder
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")   

USER = os.getenv("MY_USERNAME")
PWD = os.getenv("MY_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DBNAME = os.getenv("MY_DB", "flamingo")


pwd_enc = urllib.parse.quote_plus(PWD)
uri = f"mongodb+srv://{USER}:{pwd_enc}@cluster0.prowd2l.mongodb.net/{DBNAME}?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(uri)
mydb = myclient["flamingo"]
mycol = mydb["searches"]


if not (USER and PWD):
    raise RuntimeError("Missing MY_USERNAME or MY_PASSWORD in .env")


client = genai.Client(api_key=GEMINI_API_KEY)

# call function with arg1=word, arg2=sentence containing the word, arg3=definitions from wiktionary
def askForContext(word, sentence, definitions):
    print("in askForContext")
    prompt = "Given this sentence: \"" + sentence + "\" \nand these definitions for the word " + word + ":"

    for i in range(0, len(definitions)):
        prompt += "\n\t" + str(i+1) + ") " + definitions[i]

    prompt += "\nReturn the index of the definition that makes the most sense for the word within the context of the sentence."

    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        config=types.GenerateContentConfig(
            system_instruction="Return only the index of the correct definition."),
        contents=prompt
    )
    
    ind = int(response.text)

    
    mylist = [
    { "phrase": word, "definition": response.text},
    ]

    x = mycol.insert_many(mylist)

    doc = mycol.find_one({"_id": x.inserted_ids[0]})
    print(doc["phrase"])

    print(x.inserted_ids)

    return definitions[ind]

def main():
    w = "tester"
    d = ["testtaker", "placeholder",  "cotton swab"]
    s = "In this sentence, this word is a tester"
    askForContext(w, s, d)

main()