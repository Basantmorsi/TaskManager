from http.client import responses

from fastapi.testclient import TestClient
from main import app
from datetime import datetime
import pytest

client = TestClient(app)

Task = {
    "id": 1,
    "title": "learn fast api",
    "description": "start learning fast api to work on the assignment",
}

@pytest.fixture(autouse=True)
def before_each():
     response = client.post(
        "/reset/")
     assert response.status_code == 200

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to Our Task Manager API'}


    # id: int
    # title: str
    # description: str
    # status : Optional[Status] = Status.todo
    # priority : Optional[Priority] = Priority.low
    # tags : Optional[list[str]] = None
    # created_at :Optional[datetime]= None

def test_create_task():
    response = client.post("/tasks/", json= {
        "id": 1,
        "title": "learn fast api",
        "description": "start learning fast api to work on the assignment",
        "status" : "in_progress",
        "priority" : "medium",
        "tags" : ["python", "backend"],
        #"created_at" : datetime.now(),
    })
    assert response.status_code == 201
    assert response.json()[0]["title"] == "learn fast api"
    assert response.json()[0]["description"] == "start learning fast api to work on the assignment"
    assert response.json()[0]["status"] == "in_progress"
    assert response.json()[0]["priority"] == "medium"
    assert response.json()[0]["tags"] == ["python", "backend"]

def test_create_task_by_default():
    response = client.post("/tasks/", json= {
        "id": 2,
        "title": "learn relational Databases",
        "description": "start learning different types of DBs",
    })
    assert response.status_code == 201
    assert response.json()[0]["title"] == "learn relational Databases"
    assert response.json()[0]["description"] == "start learning different types of DBs"
    assert response.json()[0]["status"] == "todo"
    assert response.json()[0]["priority"] == "low"
    assert response.json()[0]["tags"] is None

def test_create_task_missing_title():
    response = client.post("/tasks/", json= {
        "id": 3,
        "description": "Wrong task with no title",
    })
    assert response.status_code == 422

def test_get_tasks_empty_at_start():
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert response.json() == []

def test_get_tasks_returns_all():
        client.post("/tasks/", json={
            "id": 2,
            "title": "learn relational Databases",
            "description": "start learning different types of DBs",
    })
        response = client.get("/tasks/")
        assert len(response.json()) == 1

def test_get_task_by_id():
    client.post("/tasks/", json = Task)
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["title"]  == "learn fast api"

def test_get_task_by_id_not_found():
    response = client.get("/tasks/10000")
    assert response.status_code == 404

def test_update_existing_task():
    client.post("/tasks/", json = Task)
    task_id = Task["id"]
    response = client.put(f"/tasks/{task_id}", json = {
        "id" : task_id,
        "title" : "Updated new title",
        "description" : "Updated new description",
    })
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Updated new title"
    assert response.json()[0]["description"] == "Updated new description"

def test_update_non_existing_task():
    client.post("/tasks/", json = Task)
    task_id = Task["id"]
    response = client.put(f"/tasks/{task_id}", json = {
        "id" : 5000,
        "title" : "Updated new title",
        "description" : "Updated new description",
    })
    assert response.status_code == 404