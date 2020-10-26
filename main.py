from fastapi import FastAPI, Header, HTTPException, Depends
from routers import indentity, secrets
from typing import List 
from sqlalchemy.orm import Session
from sql import crud , models, schemas
from sql.database import engine
from base.utils import get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    
#route to identity
app.include_router(
    indentity.router,
    prefix="/indentity",
    tags=["indentity"],
    responses={404: {"description": "Not found"}}
)
#route to secrets
app.include_router(
    secrets.router,
    prefix="/secrets",
    tags=["secrets"],
    responses={404: {"description": "Not found"}}
)

@app.get('/')
def getWelcome():
    return {'welcome':'secrets API'}