import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import models, database

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_db():
    models.Base.metadata.create_all(bind=database.engine)
    yield
    models.Base.metadata.drop_all(bind=database.engine)


def test_create_task(setup_db):
    # Test creating a new task through the API
    response = client.post("/tasks/", json={"title": "Develop Mobile App",
                                            "description": "Create a mobile version of the web platform",
                                            "completed": False})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Develop Mobile App"
    assert data["description"] == "Create a mobile version of the web platform"
    assert data["completed"] is False


def test_get_task(setup_db):
    # Test retrieving a task by its ID through the API
    response = client.post("/tasks/", json={"title": "Update Privacy Policy",
                                            "description": "Revise the company's privacy policy to comply with new regulations",
                                            "completed": False})
    task_id = response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Update Privacy Policy"


def test_get_tasks(setup_db):
    # Test retrieving a list of tasks through the API
    client.post("/tasks/", json={"title": "Conduct Market Research",
                                 "description": "Research the target market for the new product", "completed": False})
    client.post("/tasks/",
                json={"title": "Plan Product Launch", "description": "Develop a plan for launching the new product",
                      "completed": False})

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_update_task(setup_db):
    # Test updating an existing task through the API
    response = client.post("/tasks/", json={"title": "Hire New Developer",
                                            "description": "Interview and hire a new developer for the backend team",
                                            "completed": False})
    task_id = response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "Hire Senior Developer",
                                                     "description": "Find and hire a senior developer with 5+ years of experience",
                                                     "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Hire Senior Developer"
    assert data["completed"] is True


def test_delete_task(setup_db):
    # Test deleting a task through the API
    response = client.post("/tasks/", json={"title": "Conduct Security Audit",
                                            "description": "Perform a security audit on the new infrastructure",
                                            "completed": False})
    task_id = response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
0