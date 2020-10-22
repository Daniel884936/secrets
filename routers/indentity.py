from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from sql import crud, models, schemas
from base.utils import get_db

router = APIRouter()

@router.get('/message/{name}')
def getWelcome(name):
    return {'Hello':name}

@router.post('/register/',response_model=schemas.User)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = crud.getUser_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db= db, user = user)
  
  
@router.post('/login/{email}/{password}')
def getUser(email, password,db:Session = Depends(get_db)):
    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=401,detail='User not found')
    return user

def authenticate_user(email, password, db):
    user = crud.getUser_by_email(db,email=email)
    if not user:
        return False
    if not password == user.password:
        return False
    return user
    