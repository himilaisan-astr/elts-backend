from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(hours=1))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
