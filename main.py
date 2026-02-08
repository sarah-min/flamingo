from fastapi import FastAPI
from pydantic import BaseModel
from scraper import parse_definition, fetch_link, Word
from context import askForContext

# request body item
class requestBody(BaseModel):
    word: str
    sentence: str

app = FastAPI()

@app.get("/search/")
def search(req: requestBody):
    # call scraper on word + sentence for context 
    link = fetch_link(req.word)
    word: Word = parse_definition(link)
    def_kofs= []
    for kof in word.kof:
        for kdef in kof.definitions:
            def_kofs.append((kdef, kof))
    
    def_idx = askForContext(req.word, req.sentence, def_kofs)
    c_def = def_kofs[def_idx][0]
    c_kof = def_kofs[def_idx][1]

    return {
        "link" : link,
        "word" : req.word, # og word
        "sentence" : req.sentence, # og sentence/context
        "usage" : c_def.usage, # usage, ex. whether its aave or not, may or may not be provided
        "definition" : c_def.definition, # one line definition
        "etymology" : c_kof.etymology,
        "usage_notes" : c_kof.usage_notes, # notes on usage
        "category" : c_kof.category # verb, noun, etc
    }

def main():
    body = requestBody(
        word = "woke",
        sentence = "Remember to stay woke"
    )
    print(search(body))
    return 0

if __name__ == "__main__":
    main()