import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert: List activities
def test_get_activities():
    # Arrange: nothing needed, just call endpoint
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Arrange-Act-Assert: Sign up participant
def test_signup_for_activity():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

# Arrange-Act-Assert: Prevent duplicate signup
def test_signup_duplicate():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

# Arrange-Act-Assert: Delete participant
def test_delete_participant():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

# Arrange-Act-Assert: Delete non-existent participant
def test_delete_nonexistent_participant():
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
