from argon2 import PasswordHasher
from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt 
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from src.env import JWT_SECRET_KEY, ALGORITHM, JWT_REFRESH_SECRET_KEY

ph = PasswordHasher()

def hash_pass(password: str):
    hashed_password = ph.hash(password)
    return hashed_password

def verify_pass(password: str, hashed_password: str):
    try:
        return ph.verify(hashed_password, password)
    except Exception:
        return False
    
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, secret: str):
    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")