from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

Task = {
    "id": 1,
    "title": "learn fast api",
    "description": "start learning fast api to work on the assignment",
}

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to Our Task Manager API'}



def test_create_task():
    response = client.post("/tasks/", json= Task)
    assert response.status_code == 201
    #assert response.json()["title"] == "learn fast api"
    #assert response.json()["status"] == "todo"
    #assert response.json()["priority"] == "low"
    #assert response.json()["tags"] is None