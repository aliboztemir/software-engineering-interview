# QA - FastAPI Exercise

## Goal

The goal of providing an exercise is to evaluate the candidate's ability to solve real-world problems and demonstrate their technical skills in action.

The candidate will be required to defend their solution in the interview, justifying why they have made certain decisions to test the API.

## Description

Test a small API to manage a to-do list. The API has the following operations:

- Create a task.
- Get a task by its ID.
- Get all tasks.
- Update a task by its ID.
- Delete a task by its ID.

Each task has the following fields:

- **ID** (auto-generated, integer).
- **Title** (string).
- **Description** (string).
- **Status** (boolean, default is False).

When creating the task the following validations are applied:

- Title length validation: The task title must be between 5 and 50 characters.
- Description length validation: The task description must be at least 10 characters.

## Requirements

- Write unit tests that do not depend on infrastructure services like the database, instead use mocks.
  - What parts of the application would you unit test? The number of tests is not as relevant as the components that are tested.
- Write integration tests that use a PostgreSQL database running in Docker instead of using mocks. Tip: docker-compose can be used to do so easily.
  - What parts of the application would you unit test? The number of tests is not as relevant as the components that are tested.
- Add content to the section [6. Running tests with Poetry](#6-running-tests-with-poetry) to explain how to run the tests and generate coverage reports.
- Write a load test on one of the implemented endpoints. Tip: [Locust](https://locust.io) or [K6](https://k6.io) can used to do so easily.
  - If you can, attach a screenshot of the test report to see the endpoint response time curve as the test increases or decreases the load.
- How would you apply regression testing in this project?
- If it were up to you, what stages would the life cycle of this application include to ensure a high quality standard?
- Regarding testing, where does a unit and integration test begin and end? That is, what are their differences?
- How can you measure the code quality of this project? What metrics/characteristics make up quality?

### To watch out

The application code may present some intentional error to provide greater richness and complexity to the exercise.

## Project Structure

The basic structure of the project could be something like this or similar (not strictly the same):

```
fastapi/
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
└── tests/
│   ├── __init__.py
│   ├── test_integration.py
│   ├── test_unit.py
└── docker-compose.yaml
└── poetry.lock
└── pyproject.toml
└── README.md
```

## Initializing the project

### 1. Initialize Your Project with Poetry

```
poetry init
```

### 2. Add Dependencies

```
poetry add fastapi sqlalchemy pydantic psycopg2-binary
poetry add --dev pytest pytest-asyncio httpx
```

### 3. Check Virtual Environment

Poetry automatically creates a virtual environment for your project. You can check where Poetry has created the virtual environment with:

```
poetry env info
```

### 4. Activate the Virtual Environment

If you need to activate the virtual environment manually (for example, to run a command in it), you can do so with:

```
poetry shell
```

### 5. Running API with Poetry

Execute the following Docker command to get up and running the PostgreSQL database.

```
docker-compose up -d
```

Execute the following Poetry command to get up a server and run the API.

```
poetry run uvicorn app.main:app --reload
```

### 6. Running tests with Poetry

### Running All Tests:

```
poetry run pytest
```

### Add Test Dependencies

```
poetry add --dev pytest-cov
poetry add --dev pytest-html
```

### Generating HTML Test Report:

```
poetry run pytest --html=report.html --self-contained-html
```

### Measuring Code Coverage:

```
poetry run pytest --cov=app --cov-report=html
```

### Test Files

Unit Tests: tests/test_unit.py
Test individual functions and methods with mocks.

Component Tests: tests/test_database_component.py
Test database operations with isolated environment.

Integration Tests: tests/test_api_integration.py
Test API endpoints with a real PostgreSQL database.

End-to-End Tests: tests/test_end_to_end.py
Test the full workflow of CRUD operations through the API.

### Summary

HTML Test Report:

![image](https://github.com/user-attachments/assets/d8bcd264-118c-4681-a58e-b860d9a4d25f)


Code Coverage: 

![image](https://github.com/user-attachments/assets/a816f897-3fdd-4947-993f-d6560322123c)










