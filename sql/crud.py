from sqlalchemy.orm import Session
from . import models , schemas


def create_user(db: Session, user: schemas.UserCreate):
    #password = user.password to hash password 
    db_user = models.User(email = user.email, password=user.password, name = user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def getUser_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

    