from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils import verify_token
from src.env import JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    payload = verify_token(token, JWT_SECRET_KEY)
    return payload["sub"]

def refresh_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    payload = verify_token(token, JWT_REFRESH_SECRET_KEY)
    return payload["sub"]