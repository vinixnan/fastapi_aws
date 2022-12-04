from fastapi import FastAPI
from pymongo import MongoClient
from app.routes import router as book_router
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"Status": "API Online"}


@app.on_event("startup")
def startup_db_client():
    database_url = os.environ.get('DATABASE_URL', '127.0.0.1')
    base = "books"
    app.mongodb_client = MongoClient(database_url)
    app.database = app.mongodb_client[base]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(book_router, tags=["books"], prefix="/book")
