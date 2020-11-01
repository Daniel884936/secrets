from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ServerResult():
    def __init__(self, token= '',status='', ok= False, forceLogin= False, data='' ):
        pass
        self.token=token
        self.status = status
        self.ok = ok
        self.forceLogin = forceLogin
        self.data = data
    token=''
    status = ''
    ok = False
    forceLogin = False
    data = ''

#-----------------------------------------------------------------------------------------------------

class UserEmail(BaseModel):
    email:str
    
class UserPassword(BaseModel):
    password:str

class UserBase(UserEmail):
    name: str
        
class UserCreate(UserBase, UserPassword):
    pass

class UserLogin(UserEmail,UserPassword):
    pass
     
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
    pass
class SecretDelete(BaseModel):
    id:int

