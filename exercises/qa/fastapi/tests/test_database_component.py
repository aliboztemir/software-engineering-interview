import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models, database

# Create engine and session for the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        models.Base.metadata.drop_all(bind=engine)


def test_create_task_in_db(db):
    # Create a new task and add it to the database
    task = models.Task(title="Launch Marketing Campaign",
                       description="Coordinate the launch of the new product marketing campaign", completed=False)
    db.add(task)
    db.commit()
    db.refresh(task)

    assert task.id is not None
    assert task.title == "Launch Marketing Campaign"
    assert task.description == "Coordinate the launch of the new product marketing campaign"


def test_read_task_from_db(db):
    # Add a task and then retrieve it from the database
    task = models.Task(title="Design Website", description="Create a new design for the company website",
                       completed=False)
    db.add(task)
    db.commit()
    db.refresh(task)

    db_task = db.query(models.Task).filter(models.Task.id == task.id).first()
    assert db_task.title == "Design Website"


def test_update_task_in_db(db):
    # Create a task, update its title, and check if the update is reflected in the database
    task = models.Task(title="Prepare Annual Report", description="Draft the annual financial report", completed=False)
    db.add(task)
    db.commit()
    db.refresh(task)

    task.title = "Complete Annual Report"
    db.commit()
    db.refresh(task)

    db_task = db.query(models.Task).filter(models.Task.id == task.id).first()
    assert db_task.title == "Complete Annual Report"


def test_delete_task_in_db(db):
    # Create a task and then delete it, verifying that it no longer exists in the database
    task = models.Task(title="Organize Team Building Event",
                       description="Plan and organize the next team-building event", completed=False)
    db.add(task)
    db.commit()
    db.refresh(task)

    db.delete(task)
    db.commit()

    db_task = db.query(models.Task).filter(models.Task.id == task.id).first()
    assert db_task is None
