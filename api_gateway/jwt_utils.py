import jwt
from fastapi import HTTPException, Header
from jwt import PyJWTError

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def verify_jwt_token(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=403, detail="Invalid auth scheme")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (ValueError, PyJWTError):
        raise HTTPException(status_code=403, detail="Invalid or expired token")
