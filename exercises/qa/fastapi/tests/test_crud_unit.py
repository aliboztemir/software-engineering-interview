import warnings
import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict
from app import crud, models

# Pydantic model used in tests, adapted for Pydantic v2
class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

    model_config = ConfigDict(from_attributes=True)

def test_get_task():
    db = MagicMock(spec=Session)
    task = models.Task(id=1, title="Prepare Project Report", description="Prepare the final project report for submission", completed=False)
    db.query().filter().first.return_value = task
    result = crud.get_task(db, task_id=1)
    assert result == task

def test_get_task_not_found():
    db = MagicMock(spec=Session)
    db.query().filter().first.return_value = None
    result = crud.get_task(db, task_id=1)
    assert result is None

def test_create_task_title_too_short():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", Warning)

        db = MagicMock(spec=Session)
        task_data = TaskCreate(title="Bug", description="Fix critical bug in the user authentication flow", completed=False)
        with pytest.raises(HTTPException) as exc_info:
            crud.create_task(db=db, task=task_data)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Title length must be between 5 and 50 characters"

def test_create_task_description_too_short():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", Warning)

        db = MagicMock(spec=Session)
        task_data = TaskCreate(title="Implement Payment Gateway", description="Setup", completed=False)
        with pytest.raises(HTTPException) as exc_info:
            crud.create_task(db=db, task=task_data)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Description length must be at least 10 characters"

def test_create_task_success():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", Warning)

        db = MagicMock(spec=Session)
        task_data = TaskCreate(title="Develop User Dashboard", description="Design and develop the user dashboard interface", completed=False)
        task = crud.create_task(db=db, task=task_data)
        db.add.assert_called_once()
        db.commit.assert_called_once()
        db.refresh.assert_called_once()
        assert task.title == task_data.title
        assert task.description == task_data.description

def test_update_task():
    db = MagicMock(spec=Session)
    existing_task = models.Task(id=1, title="Write Unit Tests", description="Write unit tests for the API endpoints", completed=False)
    db.query().filter().first.return_value = existing_task
    task_data = TaskCreate(title="Write and Review Unit Tests", description="Complete and review unit tests for all API endpoints", completed=True)
    updated_task = crud.update_task(db=db, task=task_data, task_id=1)
    assert updated_task.title == "Write and Review Unit Tests"
    assert updated_task.completed is True

def test_delete_task():
    db = MagicMock(spec=Session)
    task = models.Task(id=1, title="Clean up Development Branch", description="Remove unused branches and clean up the development environment", completed=False)
    db.query().filter().first.return_value = task
    deleted_task = crud.delete_task(db=db, task_id=1)
    db.delete.assert_called_once_with(task)
    db.commit.assert_called_once()
    assert deleted_task == task
