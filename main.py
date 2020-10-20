from fastapi import FastAPI, Header, HTTPException, Depends
from routers import indentity

app = FastAPI()

async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

app.include_router(
    indentity.router,
    prefix="/indentity",
    tags=["indentity"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)