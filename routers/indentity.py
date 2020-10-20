from fastapi import APIRouter

router = APIRouter()

@router.get('/message/{name}')
def getWelcome(name):
    return {'Hello':name}


@router.post('regiter/{name}/{email}/{password}')
def register(name,email,password):
  pass