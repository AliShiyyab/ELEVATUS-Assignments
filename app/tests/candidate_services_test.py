from fastapi.testclient import TestClient

from app.database_configration.db_configration import connect_to_mongo, disconnect_to_mongo
from app.services.services import UserService
from main import app
import pytest


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
async def test_db():
    db = connect_to_mongo()
    try:
        yield db
    finally:
        await disconnect_to_mongo()


def test_create_and_delete_candidate(test_app, test_db):
    candidate_data = {
        "first_name": "Ali",
        "last_name": "Shiyyab",
        "email": "aliakefsh@gmail.com",
        "uuid": "1",
        "career_level": "Mid-Senior",
        "job_major": "Software Engineer",
        "years_of_experience": 3,
        "degree_type": "Bachelor degree in computer information system",
        "skills": ["Python Flask", "Java SpringBoot", "JavaScript", "React", "NextJS", "MariaDB", "MongoDB"],
        "nationality": "Jordanian",
        "city": "Amman",
        "salary": 1000,
        "gender": "Male",
    }
    response = test_app.post("/candidate", json=candidate_data)
    assert response.status_code == 201

    updated_data = {
        "first_name": "Ali",
        "last_name": "Akef",
        "email": "ali.akef@liwwa.com",
        "uuid": "1",
        "career_level": "Mid-Senior",
        "job_major": "Software Engineer",
        "years_of_experience": 3,
        "degree_type": "Bachelor degree in computer information system",
        "skills": ["Python Flask", "Java SpringBoot", "JavaScript", "React", "NextJS", "MariaDB", "MongoDB"],
        "nationality": "Jordanian",
        "city": "Amman",
        "salary": 1000,
        "gender": "Male",
    }
    response = test_app.put("/candidate/1", json=updated_data)
    assert response.status_code == 201

    response = test_app.delete("/candidate/{aliakefsh@gmail.com}")
    assert response.status_code == 204


def test_create_user(test_app, test_db):
    user_data = {
        "first_name": "Ali",
        "last_name": "Shiyyab",
        "email": "aliakefsh@gmail.com",
        "uuid": "123"
    }
    response = test_app.post("/user", json=user_data)
    assert response.status_code == 201
