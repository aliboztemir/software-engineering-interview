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


def test_crud_operations(setup_db):
    # End-to-end test of creating, reading, updating, and deleting a task
    response = client.post("/tasks/", json={"title": "Set Up CI/CD Pipeline",
                                            "description": "Implement continuous integration and deployment for the project",
                                            "completed": False})
    assert response.status_code == 200
    task_id = response.json()["id"]

    # Verify that the task was created successfully
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Set Up CI/CD Pipeline"

    # Update the task and verify the update
    response = client.put(f"/tasks/{task_id}",
                          json={"title": "Complete CI/CD Setup", "description": "Finalize and test the CI/CD pipeline",
                                "completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == "Complete CI/CD Setup"
    assert response.json()["completed"] is True

    # Delete the task and verify the deletion
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404


def test_create_multiple_tasks(setup_db):
    # Create multiple tasks
    tasks = [
        {"title": "Develop Mobile App", "description": "Create the mobile version of the app", "completed": False},
        {"title": "Design User Interface", "description": "Design the new UI for the app", "completed": False},
        {"title": "Conduct User Testing", "description": "Run user testing sessions to gather feedback",
         "completed": False}
    ]

    for task in tasks:
        response = client.post("/tasks/", json=task)
        assert response.status_code == 200

    # Verify that all tasks were created successfully
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_update_task_to_completed(setup_db):
    # Create a task
    response = client.post("/tasks/", json={"title": "Write Documentation",
                                            "description": "Complete the user documentation for the project",
                                            "completed": False})
    task_id = response.json()["id"]

    # Mark the task as completed
    response = client.put(f"/tasks/{task_id}", json={"title": "Write Documentation",
                                                     "description": "Complete the user documentation for the project",
                                                     "completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_nonexistent_task(setup_db):
    # Try to delete a task that doesn't exist
    response = client.delete("/tasks/9999")
    assert response.status_code == 404


def test_create_task_with_invalid_data(setup_db):
    # Try to create a task with invalid data (e.g., title too short)
    response = client.post("/tasks/", json={"title": "Sh", "description": "Short title", "completed": False})
    assert response.status_code == 400
    assert response.json()["detail"] == "Title length must be between 5 and 50 characters"


def test_get_tasks_with_pagination(setup_db):
    # Create multiple tasks
    for i in range(15):
        client.post("/tasks/",
                    json={"title": f"Task {i + 1}", "description": f"Description for task {i + 1}", "completed": False})

    # Get the first 10 tasks with pagination
    response = client.get("/tasks/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10

    # Get the next 5 tasks
    response = client.get("/tasks/?skip=10&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
