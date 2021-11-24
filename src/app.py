from fastapi import FastAPI, HTTPException
import requests

from database import RandomPasteBin
from models import Text, TextWithId


app = FastAPI()
db = RandomPasteBin()


@app.get("/texts", response_model=TextWithId)
def read_rand_text():
    try:
        ret = db.get_rand_text()

        if ret['id'] < 0:
            raise HTTPException(404, ret['text'])

        return ret
    except requests.ConnectionError:
        raise HTTPException(404, "PasteBin server is not availvable")


@app.post("/texts")
def write_text(text: Text):
    try:
        db.insert_text(text.dict())
    except requests.ConnectionError:
        raise HTTPException(404, "PasteBin server is not availvable")
