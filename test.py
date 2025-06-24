import requests

def test_login(email, password):
    url = "http://52.203.72.116:8080/login"
    payload = {
        "User_mail": email,
        "password": password
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        token = response.json().get("token")
        print(f"Loggin success! Token:\n{token}")
    else:
        print(f"Error to loggin: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    
    test_email = "allan2"
    test_password = "1234"
    test_login(test_email, test_password)
