from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sql import crud, models, schemas
from base.utils import get_db
from base.token import Token
import datetime

router = APIRouter()

@router.post('create/{title}/{description}/{monetaryValue}/{date}/{place}/{lat}/{log}/{token}')
def create(title,description,monetaryValue,date,place,lat,log,token, db:Session = Depends(get_db)):
   validateFloat(monetaryValue, 'monetary value')
   validateFloat(lat, 'lat')
   validateFloat(lat, 'log')
   datetimeParsed = parseToDateTime(date)
   tokenValid = token_is_valid(token)
   if tokenValid:
        userRequest = getUser(db,tokenValid)
        if userRequest:
            secret:schemas.SecretCreate= schemas.SecretCreate(title = title, description = description, monetaryValue= monetaryValue
                                                        ,date = datetimeParsed, place= place, lat = lat, log = log)
            crud.crate_secret(db, secret, userRequest.id)
   return{'status':'sucess'}
    
    

@router.get('getSecrestsByUser/{token}')
def getSecrests_By_User(token, db:Session=Depends(get_db)):
    tokenValid = token_is_valid(token)
    if tokenValid:
        userRequest = getUser(db,tokenValid)
        if userRequest:
            items = crud.getSecrets_by_user(db, userRequest.id)
    return items


@router.delete('delete/{idSecret}/{token}')
def delete(idSecret,token, db:Session = Depends(get_db)):
    tokenValid = token_is_valid(token)
    if tokenValid:
        userRequest = getUser(db,tokenValid)
        if userRequest:
            crud.delete_secret(db, idSecret)      
    return{'status':'sucess'}


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
    
    
def validateFloat(number, invalidNumberMsg):
    try:
        number = float(number)
    except:
        raise HTTPException(status_code=400,detail=f"invalid value: {invalidNumberMsg}")
    

def parseToDateTime(datetimeParse):
    try:
        dateTimeParsed = datetime.datetime.strptime(datetimeParse,'%Y-%m-%d %H:%M:%S.%f')
        return dateTimeParsed
    except:
        raise HTTPException(status_code=400,detail=f"invalid value: date, format valid: YYYY-mm-dd HH:MM:SS.ff ")
    pass