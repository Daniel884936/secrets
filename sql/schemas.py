from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email:str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id:int
    
    class Config:
        orm_mode = True
        
#-----------------------------------------------------------------------------------------------------

class SecretBase(BaseModel):
    title: str
    description:str
    monetaryValue:float
    date:datetime
    place:str
    lat:float
    log:float

class SecretCreate(SecretBase):
    #idUser: int
    pass

class Secret(SecretBase):
    id:int
    
    class Config:
        orm_mode = True