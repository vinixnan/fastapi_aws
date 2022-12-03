from typing import Union
from fastapi import FastAPI
from pymongo import MongoClient
import datetime
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    database_url = os.environ.get('DATABASE_URL')
    client = MongoClient(database_url, 27017)
    db = client.test_database
    post = {"idx": item_id,
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}
    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    return {"item_id": item_id, "q": q, "id": post_id}
