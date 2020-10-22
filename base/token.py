import jwt

#Secret key for token
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0'
ALGORITHM= 'HS256'

class Token:
    #this is the firm fo all tokens created 
    def generateToken(self, sub, userName, email):
        userDict: dict = {
            "sub": sub,
            "name": userName,
            "email": email
        }
        encoded_jwt  = jwt.encode(userDict, SECRET_KEY, ALGORITHM)
        return encoded_jwt
    
    