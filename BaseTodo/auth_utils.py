import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from decouple import config

JWT_KEY = config("JWT_KEY")

class AuthJwtCsrf():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   
    secret_key = JWT_KEY

    def generate_hashed_password(self, password) -> str:
        self.pwd_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def encode_jwt(self, email) -> str:
        payload = {
            "sub": "email",
            "exp": datetime.utcnow() + timedelta(days=0, minutes=5),
            "iat": datetime.utcnow()
        }

        return jwt.encode(
            payload, 
            self.secret_key, 
            algorithm="HS256"
            )  
    
    def decode_jwt(self, token) -> str:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="The JWT has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="JWT is not valid")
    