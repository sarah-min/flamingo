from fastapi import FastAPI
from pydantic import BaseModel

# request body item
class requestBody(BaseModel):
    word: str
    sentence: str

app = FastAPI()

@app.get("/search/")
async def search(req: requestBody):
    # call scraper on word + sentence for context 

    # scraper calls context, returns definition (str)
    return "ret"


def main():
    return 0


if __name__ == "__main__":
    main()