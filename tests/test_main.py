import pytest
from fastapi.testclient import TestClient
import httpx
from main import app
import json

client = TestClient(app)

@pytest.fixture
def user_data():
    return {
        "username": "testuser7",
        "email": "testuser7@abc.com",
        "password": "testuser7"
    }

@pytest.fixture
def token(user_data):
    # Signup first (ignore if user exists)
    client.post("signup", json=user_data)
    # Login to get token
    response = client.post(
        "/login",
        data={"username": user_data["username"], "password": user_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]

def test_signup(user_data):
    response = client.post("signup", json=user_data)
    assert response.status_code in (200, 400)  # 400 if user exists

def test_login(user_data):
    response = client.post(
        "/login",
        data={"username": user_data["username"], "password": user_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_task(token):
    task_data = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/tasks/createTask", json=task_data, headers=headers)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["title"] == task_data["title"]
    assert json_resp["description"] == task_data["description"]

def test_getAlltasks(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/tasks/getAllTasks", headers=headers)
    assert response.status_code in (200,400,405)
    assert response.json()
