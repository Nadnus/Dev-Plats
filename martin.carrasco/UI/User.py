from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative.api import ConcreteBase

class User(ConcreteBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(50))

user1 = User(id=1,name="ed",fullname="Ed Jones", password="hola123")
user2 = User(id=2,name="jb",fullname="Je Bell", password="bye123")
session.add(user1)
session.add(user2)
sessio
session.commit()
