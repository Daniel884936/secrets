from sqlalchemy.orm import Session
from sqlalchemy import update
from . import models , schemas

#SECTION USERS---------------------------------------------------------------------------------

def create_user(db: Session, user: schemas.UserCreate):
    #password = user.password to hash password 
    db_user = models.User(email = user.email, password=user.password, name = user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    #return db_user

def getUser_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
    
def getUser_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def updateUser(db:Session, userToUpdate, email, name, password):
    #userToUpdate is the memory postion about current user
    userToUpdate.name = name
    userToUpdate.email = email
    userToUpdate.password = password
    db.commit()
    return userToUpdate

#SECTION SECRETS---------------------------------------------------------------------------------

def crate_secret(db: Session, secret: schemas.SecretCreate, idUser):
    db_secret = models.Secret(**secret.dict(),owner_id =  idUser)
    db.add(db_secret)
    db.commit()
    db.refresh(db_secret)
    
    
def getSecrets_by_user(db:Session, idUser:int):
    items =  db.query(models.Secret).join(models.User).filter(models.Secret.owner_id == idUser).all()
    return  items

def delete_secret(db:Session, idSecret:int):
    db.query(models.Secret).filter(models.Secret.id==idSecret).delete()
    db.commit()
    pass
    
