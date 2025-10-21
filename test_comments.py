# tests/test_comments.py
import json
import pytest
# from app import create_app
from config import TestConfig
from db import db
from models import Comment

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_add_and_get_comments(client):
    # add comment to task 1
    resp = client.post("/api/tasks/1/comments", json={"text": "First comment", "author": "Alice"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["task_id"] == 1
    assert data["text"] == "First comment"

    # get comments for task 1
    resp = client.get("/api/tasks/1/comments")
    assert resp.status_code == 200
    arr = resp.get_json()
    assert isinstance(arr, list)
    assert len(arr) == 1
    assert arr[0]["text"] == "First comment"

def test_update_comment(client):
    # create
    resp = client.post("/api/tasks/2/comments", json={"text": "To update", "author": "Bob"})
    comment = resp.get_json()
    cid = comment["id"]

    # update
    resp = client.put(f"/api/comments/{cid}", json={"text": "Updated text"})
    assert resp.status_code == 200
    updated = resp.get_json()
    assert updated["text"] == "Updated text"

def test_delete_comment(client):
    resp = client.post("/api/tasks/3/comments", json={"text": "To delete"})
    cid = resp.get_json()["id"]

    resp = client.delete(f"/api/comments/{cid}")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Comment deleted"

    # ensure it's gone
    resp = client.get("/api/tasks/3/comments")
    assert resp.status_code == 200
    assert resp.get_json() == []
