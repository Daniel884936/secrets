from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sql import crud, models, schemas
from base.utils import get_db, validate_if_logged
from base.token import Token
import datetime

router = APIRouter()

@router.post('create/{token}')
def create(secret:schemas.SecretCreate,token, db:Session = Depends(get_db)):
   tokenValid = token_is_valid(token)
   if tokenValid:
        userRequest = getUser(db,tokenValid)
        if userRequest:
            crud.crate_secret(db, secret, userRequest.id)
        if not validate_if_logged(db,userRequest.id):
            return schemas.ServerResult(status='not logged', ok=False, forceLogin= False)
        return schemas.ServerResult(status='sucess', ok=True, forceLogin= True)
    
    

@router.get('getSecrestsByUser/{token}')
def getSecrests_By_User(token, db:Session=Depends(get_db)):
    tokenValid = token_is_valid(token)
    if tokenValid:
        userRequest = getUser(db,tokenValid)
        if userRequest:
            items = crud.getSecrets_by_user(db, userRequest.id)
        if not validate_if_logged(db,userRequest.id):
            return schemas.ServerResult(status='not logged', ok=False, forceLogin= False)
    return schemas.ServerResult(status='sucess', ok=True, forceLogin= True, data=items)


@router.delete('delete/{token}')
def delete(secret:schemas.SecretDelete,token, db:Session = Depends(get_db)):
    tokenValid = token_is_valid(token)
    if tokenValid:
        userRequest = getUser(db,tokenValid)
        if userRequest:
            crud.delete_secret(db, secret.id)    
        if not validate_if_logged(db,userRequest.id):
            return schemas.ServerResult(status='not logged', ok=False, forceLogin= False)  
    return schemas.ServerResult(status='sucess', ok=True, forceLogin= True)


def token_is_valid(token):
    tokenInstance = Token()
    tokenDecoded = tokenInstance.decodeToken(token)
    if not tokenDecoded:
        raise HTTPException(status_code=401, detail={"unauthorized"})
    return tokenDecoded


def getUser(db:Session, token):
    userRequest = crud.getUser_by_id(db,token['sub'])
    if not userRequest:
        raise HTTPException(status_code=401, detail={"user not found"})
    return userRequest
