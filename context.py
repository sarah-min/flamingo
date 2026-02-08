from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()

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
    
    ind = int(response.text)-1

    # returns tuple <word, def>
    return word, definitions[ind]

def main():
    w = "tester"
    d = ["testtaker", "placeholder",  "cotton swab"]
    s = "In this sentence, this word is a tester"
    askForContext(w, s, d)

main()