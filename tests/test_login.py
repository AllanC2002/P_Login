import pytest
from unittest.mock import patch, MagicMock
from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("services.functions.conection_accounts")
def test_login_success(mock_conection, client):
    # Simmulate a database connection
    mock_session = MagicMock()
    mock_conection.return_value = mock_session

    # Simulate a user in the database
    fake_user = MagicMock()
    fake_user.Status = 1
    fake_user.Password = "hashed123"
    fake_user.Id_User = 1
    fake_user.User_mail = "juan@example.com"
    mock_session.query().filter().one.return_value = fake_user

    # Simmulate the password hashing function
    from services.functions import hash_password
    plain_password = "mipassword"
    fake_user.Password = hash_password(plain_password)

    response = client.post("/login", json={
        "User_mail": "juan@example.com",
        "password": plain_password
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert "token" in json_data
