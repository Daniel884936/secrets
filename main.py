from fastapi import FastAPI, Header, HTTPException, Depends
from routers import indentity, secrets
from typing import List 
from sqlalchemy.orm import Session
from sql import crud , models, schemas
from sql.database import engine
from base.utils import get_db
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
    
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
def root():
    return {'welcome':'secrets API'}