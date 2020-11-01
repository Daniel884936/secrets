from sql.database import SessionLocal
from sql import crud
from fastapi import HTTPException
from sqlalchemy.orm import Session 
from base.token import Token
from sql import models

# Dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

#validations
def validate_if_logged(db: Session, idUser):
    #se esta retornanco un none....
    token_db:models.Token = crud.getToken_db(db,idUser)
    tokenDecoded  = Token().decodeToken(token_db.value)
    """ if not tokenDecoded:
        raise HTTPException(status_code=400,detail='bad request') """
    isLogged = tokenDecoded["forceLogin"]
    print(isLogged)
    if isLogged:
        return True
    return False
    
 