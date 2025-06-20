from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# DB Accounts
class User(Base):
    __tablename__ = 'Users'
    Id_User = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100))
    Lastname = Column(String(100))
    User_mail = Column(String(100), unique=True)
    Password = Column(String(100))
    Status = Column(Integer, CheckConstraint('Status IN (0, 1)'))

