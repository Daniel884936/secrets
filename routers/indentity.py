from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from sql import crud, models, schemas
from base.utils import get_db
from base.token import Token

router = APIRouter()
""" @router.post('/register/',response_model=schemas.User)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = crud.getUser_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db= db, user = user) """
  
@router.post('/register/{name}/{email}/{password}')
def create_user(name, email,password, db:Session = Depends(get_db)):
    user: schemas.UserCreate = schemas.UserCreate(name= name, email=email,password=password)
    db_user = crud.getUser_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    crud.create_user(db= db, user = user)
    return{'status':'sucess, user created'}
  
  
@router.post('/login/{email}/{password}')
def getUser(email, password,db:Session = Depends(get_db)):
    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=401,detail='User not found')
    userToken = Token()
    token = userToken.generateToken(sub=user.id, userName=user.name, email= user.email)
    return {
        'status': 'sucess',
        'token' : token
    }

@router.put('/useredit/{oldemail}/{name}/{email}')
def edit(oldEmail,name, email, db: Session = Depends(get_db)):
    userRquest = crud.getUser_by_email(db, email= oldEmail)
    if not userRquest:
        raise HTTPException(status_code=401, detail='User not found')
    #userToUpdate is the memory position
    userUpdated = crud.updateUser(db,userToUpdate= userRquest, email = email, name = name)
    userToken = Token()
    newToken = userToken.generateToken(sub=userUpdated.id,userName=userUpdated.name,
                                       email=userUpdated.email)
    return {'status':'sucess',
            'token': newToken}


@router.put('/changepassword/{oldpassword}/{token}')
def change_password(oldpassword,token):
    tokenInstance = Token()
    user = tokenInstance.decodeToken(token)
    if not user:
        raise HTTPException(status_code=401, detail='unauthorized')
    return user

#TODO
def authenticate_user(email, password, db):
    user = crud.getUser_by_email(db,email=email)
    if not user:
        return False
    if not password == user.password:
        return False
    return user

