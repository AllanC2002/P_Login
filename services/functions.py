import jwt
import datetime
from sqlalchemy.exc import NoResultFound
from models.models import User
from conections.mysql import conection_accounts
import hashlib
import os

key = os.getenv("SECRET_KEY")

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def login_user(user_mail, password):
    session = conection_accounts()

    try:
        user = session.query(User).filter(User.User_mail == user_mail).one()

        if user.Status != 1:
            return {"error": "User is inactive"}, 403

        hashed_input = hash_password(password)
        if user.Password != hashed_input:
            return {"error": "Invalid credentials"}, 401

        payload = {
            "user_id": user.Id_User,
            "email": user.User_mail,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }

        token = jwt.encode(payload, key, algorithm="HS256")
        return {"token": token}, 200

    except NoResultFound:
        return {"error": "User not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
