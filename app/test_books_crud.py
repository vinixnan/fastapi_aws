from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo import MongoClient
from app.routes import router as book_router
import os
from faker import Faker

app = FastAPI()
fake = Faker()
app.include_router(book_router, tags=["books"], prefix="/book")


@app.on_event("startup")
async def startup_event():
    database_url = os.environ.get('DATABASE_URL', '127.0.0.1')
    base = "books_test"
    app.mongodb_client = MongoClient(database_url)
    app.database = app.mongodb_client[base]


@app.on_event("shutdown")
async def shutdown_event():
    app.database.drop_collection("books_test")
    app.mongodb_client.close()


def test_create_book():
    with TestClient(app) as client:
        name_author = fake.name()
        name_title = fake.catch_phrase()
        response = client.post(
            "/book/", json={"title": name_title, "author": name_author, "synopsis": "..."})
        assert response.status_code == 201

        body = response.json()
        assert body.get("title") == name_title
        assert body.get("author") == name_author
        assert body.get("synopsis") == "..."
        assert "_id" in body


def test_create_book_missing_title():
    with TestClient(app) as client:
        response = client.post(
            "/book/", json={"author": "Miguel de Cervantes", "synopsis": "..."})
        assert response.status_code == 422


def test_create_book_missing_author():
    with TestClient(app) as client:
        response = client.post(
            "/book/", json={"title": "Don Quixote", "synopsis": "..."})
        assert response.status_code == 422


def test_create_book_missing_synopsis():
    with TestClient(app) as client:
        response = client.post(
            "/book/", json={"title": "Don Quixote", "author": "Miguel de Cervantes"})
        assert response.status_code == 422


def test_get_book():
    with TestClient(app) as client:
        new_book = client.post(
            "/book/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."}).json()

        get_book_response = client.get("/book/" + new_book.get("_id"))
        assert get_book_response.status_code == 200
        assert get_book_response.json() == new_book


def test_get_book_unexisting():
    with TestClient(app) as client:
        get_book_response = client.get("/book/unexisting_id")
        assert get_book_response.status_code == 404


def test_update_book():
    with TestClient(app) as client:
        name_author = fake.name()
        name_title = fake.catch_phrase()
        name_title_updated = fake.catch_phrase()
        new_book = client.post(
            "/book/", json={"title": name_title, "author": name_author, "synopsis": "..."}).json()

        response = client.put("/book/" + new_book.get("_id"),
                              json={"title": name_title_updated})
        assert response.status_code == 200
        assert response.json().get("title") == name_title_updated


def test_delete_book():
    with TestClient(app) as client:
        name_author = fake.name()
        name_title = fake.catch_phrase()
        new_book = client.post(
            "/book/", json={"title": name_title, "author": name_author, "synopsis": "..."}).json()

        delete_book_response = client.delete("/book/" + new_book.get("_id"))
        assert delete_book_response.status_code == 204


def test_delete_book_unexisting():
    with TestClient(app) as client:
        delete_book_response = client.delete("/book/unexisting_id")
        assert delete_book_response.status_code == 404
