from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from sql import crud, models, schemas
from base.utils import get_db, validate_if_logged
from base.token import Token

router = APIRouter()

@router.post('/register/')
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = crud.getUser_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    user_created = crud.create_user(db= db, user = user)
    token = Token().generateToken(user_created.id,user_created.name,user_created.email,False)
    crud.create_token(db,token,user_created.id)
    return schemas.ServerResult(status='sucess, user created', ok=True)

  
@router.post('/login/')
def getUser(user:schemas.UserLogin,db:Session = Depends(get_db)):
    userAuth = authenticate_user(**user.dict(), db= db)
    if not userAuth:
        raise HTTPException(status_code=401,detail='User not found')
    tokenToSearch = Token().generateToken(sub=userAuth.id, userName=userAuth.name, 
                                  email= userAuth.email,forceLogin=False)
    tokenToUpdate = crud.getToken_db(db,tokenToSearch)
    token = Token().generateToken(sub=userAuth.id, userName=userAuth.name, 
                                  email= userAuth.email,forceLogin=True)
    crud.update_token_user(db,token,userAuth.id)
    return schemas.ServerResult(status='sucess', ok=True, forceLogin= True ,token=token)




@router.put('/userEditNameEmail/{token}')
def edit_name_email(user:schemas.UserBase,token, db: Session = Depends(get_db)):
    tokenAuth = Token().decodeToken(token)
    if not tokenAuth:
       raise HTTPException(status_code=401, detail="unauthorized") 
    userRquest = crud.getUser_by_email(db, email= tokenAuth['email'])
    if not userRquest:
        raise HTTPException(status_code=401, detail='User not found')
    if not validate_if_logged(db,userRquest.id):
        return schemas.ServerResult(status='not logged', ok=False, forceLogin= False)
    #'userToUpdate' is the memory position
    userUpdated = crud.updateUser(db,userToUpdate= userRquest, **user.dict(),password=userRquest.password)
    newToken = Token().generateToken(sub=userUpdated.id,userName=userUpdated.name,
                                       email=userUpdated.email, forceLogin=True)
    #update to login
    crud.update_token_user(db,newToken, userRquest.id)
    return schemas.ServerResult(status='sucess', ok=True, forceLogin= True ,token=newToken)


@router.put('/userChangepassword/{token}')
def change_password( user:schemas.UserPassword,token, db:Session = Depends(get_db)):
    userAuth = Token().decodeToken(token)
    if not userAuth:
        raise HTTPException(status_code=401, detail='unauthorized')
    userToUpdate = crud.getUser_by_email(db, userAuth['email'])
    if not userToUpdate:
        raise HTTPException(status_code=401, detail='user not found')
    if not validate_if_logged(db,userToUpdate.id):
        return schemas.ServerResult(status='not logged', ok=False, forceLogin= False)
    userUpdated = crud.updateUser(db,userToUpdate= userToUpdate,email=userToUpdate.email,name=userToUpdate.name,
                                  password=user.password)
    return schemas.ServerResult(status='sucess', ok=True, forceLogin= True)


@router.post('/logout/{token}')
def funcname(token, db:Session = Depends(get_db)):
    tokenAuth = Token().decodeToken(token)
    if not tokenAuth:
        raise HTTPException(status_code=401, detail='unauthorized')
    userRquest = crud.getUser_by_email(db, email= tokenAuth['email'])
    if not userRquest:
        raise HTTPException(status_code=401, detail='User not found')
    tokenLogout = Token().generateToken(userRquest.id, userRquest.name,userRquest.name,False)
    crud.update_token_user(db,tokenLogout,userRquest.id)
    return schemas.ServerResult(status='sucess', ok=True, forceLogin= False)


def authenticate_user(email, password, db):
    user = crud.getUser_by_email(db,email=email)
    if not user:
        return False
    if not password == user.password:
        return False
    return user

