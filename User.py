from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative.api import ConcreteBase

class User(ConcreteBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(50))
