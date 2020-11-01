from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, index= True)
    name = Column(String)
    email = Column(String, unique=True, index= True)
    password = Column(String)
    secrets = relationship("Secret", back_populates="owner")
    token = relationship("Token", back_populates= "owner")
    
    
class Secret(Base):
    __tablename__ = 'secrets'
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    description = Column(String)
    monetaryValue = Column(Float)
    date = Column(DateTime)
    place  = Column(String)
    lat = Column(Float)
    log = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner  = relationship("User", back_populates="secrets")
    

class Token(Base):
    __tablename__= 'token'
    id = Column(Integer,primary_key=True, index= True)
    value = Column(String, index=True)
    owner_id = Column(Integer,ForeignKey('users.id'))
    owner = relationship("User", back_populates="token")
    