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


client = genai.Client()

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


