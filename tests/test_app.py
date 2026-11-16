import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_activity(monkeypatch):
    name = "Test Activity"
    monkeypatch.setitem(
        activities,
        name,
        {
            "description": "An activity used in tests",
            "schedule": "Mondays",
            "max_participants": 10,
            "participants": [],
        },
    )
    return name


def test_get_activities_returns_activity(client, test_activity):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()[test_activity]["participants"] == []


def test_signup_adds_participant(client, test_activity):
    # Arrange
    email = "student@example.com"

    # Act
    response = client.post(
        f"/activities/{test_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {test_activity}"
    }
    assert activities[test_activity]["participants"] == [email]


def test_delete_removes_participant(client, test_activity):
    # Arrange
    email = "student@example.com"
    activities[test_activity]["participants"].append(email)

    # Act
    response = client.delete(
        f"/activities/{test_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Removed {email} from {test_activity}"
    }
    assert activities[test_activity]["participants"] == []
