import pytest
from unittest.mock import patch, MagicMock
from main import app
import os

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = True
    with app.test_client() as client:
        yield client

@patch("services.functions.jwt.encode") 
@patch("services.functions.conection_accounts") 
def test_login_success(mock_conection, mock_jwt_encode, client):
    # Simulate SECRET_KEY
    os.environ["SECRET_KEY"] = "test-secret-key"

    # Simulate response from jwt.encode
    mock_jwt_encode.return_value = "fake.jwt.token"

    # Simulate database session and user
    mock_session = MagicMock()
    mock_conection.return_value = mock_session

    fake_user = MagicMock()
    fake_user.Status = 1
    fake_user.Id_User = 1
    fake_user.User_mail = "juan@example.com"

    from services.functions import hash_password
    plain_password = "mipassword"
    fake_user.Password = hash_password(plain_password)

    mock_session.query().filter().one.return_value = fake_user

    response = client.post("/login", json={
        "User_mail": "juan@example.com",
        "password": plain_password
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["token"] == "fake.jwt.token"
