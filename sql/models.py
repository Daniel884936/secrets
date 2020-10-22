from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer,primary_key=True, index= True)
    name = Column(String)
    email = Column(String, unique=True, index= True)
    password = Column(String)
    #token = relationship("Token", back_populates="owner")

""" class Token(Base):
    __tablename__= 'UserToken'
    id = Column(Integer,primary_key=True, index= True)
    value = Column(String)
    owner = relationship("User", back_populates="token")
     """