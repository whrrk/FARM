from fastapi.encoders import jsonable_encoder
import jwt
from fastapi import HTTPException, Request
from passlib.context import CryptContext
from datetime import datetime, timedelta
from decouple import config
from fastapi_csrf_protect import CsrfProtect

JWT_KEY = config("JWT_KEY")

class AuthJwtCsrf():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   
    secret_key = JWT_KEY

    def generate_hashed_password(self, password) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def encode_jwt(self, email) -> str:
        payload = {
            "sub": email,
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
    
    def verify_jwt(self, request:Request) -> str:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(
                status_code=401, detail="JWT token is missing")

        _, _, value = token.partition(" ")
        #_bear _csrf 
        subject = self.decode_jwt(value)
        return subject
    
    def verify_update_jwt(self, request) -> tuple[str, str]:
        subject = self.verify_jwt(request)
        new_token = self.encode_jwt(subject)
        return subject, new_token
    
    async def verify_csrf_update_jwt(self, request: Request, csrf_protect: CsrfProtect) -> tuple[str, str]:
        await csrf_protect.validate_csrf(request)
        raw_token = request.cookies.get("access_token")
        
        if not raw_token:
            raise HTTPException(status_code=401, detail="No token")

        if raw_token.startswith("Bearer "):
            raw_token = raw_token.replace("Bearer ", "")
        
        payload = jwt.decode(raw_token, self.secret_key, algorithms=["HS256"])
        email = payload.get("sub")
        
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        new_token = self.encode_jwt(email)

        return email, new_token