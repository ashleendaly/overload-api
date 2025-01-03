from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, StringConstraints
from sqlmodel import select
from typing_extensions import Annotated

from src.models import User 
from src.utils import create_access_token, create_refresh_token, hash_pass, verify_pass
from src.db import create_db_and_tables, SessionDep
from src.middleware import get_current_user, refresh_current_user


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return "Active"

class Register(BaseModel):
    username: str
    password: Annotated[str, StringConstraints(min_length=8,max_length=20)]
    email: EmailStr

@app.post("/register/")
async def register(user: Register, session: SessionDep):
    hash = hash_pass(user.password)
    new_user = User(username=user.username, email=user.email, password=hash)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

class Login(BaseModel):
    username: str
    password: str

@app.post("/login/")
async def login(login_request: Login, session: SessionDep):
    user = session.exec(select(User).where(User.username == login_request.username)).first()
    if not user or not verify_pass(login_request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})

    return {"access_token": access_token, "refresh_token": refresh_token}

@app.post("/refresh/")
async def refresh_token(username: str = Depends(refresh_current_user)):    
    access_token = create_access_token({"sub": username})
    return {"access_token": access_token}

@app.get("/protected/")
async def protected_route(username: str = Depends(get_current_user)):
    return {"message": "Access granted", "username": username}
