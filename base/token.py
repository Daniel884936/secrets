import jwt

class Token:
    #Secret key for token
    SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0'
    ALGORITHM= 'HS256'
    
    #this is the film to all tokens created 
    def generateToken(self, sub, userName, email):
        userDict: dict = {
            "sub": sub,
            "name": userName,
            "email": email
        }
        encoded_jwt  = jwt.encode(userDict, self.SECRET_KEY, self.ALGORITHM)
        return encoded_jwt
    

    def decodeToken(self,token):
        try:
            user = jwt.decode(token,self.SECRET_KEY, self.ALGORITHM)
            return user
        except:
             return False
          
        
    
    