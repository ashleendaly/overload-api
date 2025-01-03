from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, StringConstraints
from sqlmodel import select
from typing_extensions import Annotated

from src.models import User 
from src.utils import create_access_token, create_refresh_token, hash_pass, verify_pass
from src.db import create_db_and_tables, SessionDep
from src.middleware import authorize_refresh, authorize_request


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return "Active"

class Register(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8,max_length=20)]

@app.post("/register/")
async def register(user: Register, session: SessionDep):
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists.",
        )
    
    hash = hash_pass(user.password)
    
    new_user = User(email=user.email, password=hash)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user


class Login(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8,max_length=20)]

@app.post("/login/")
async def login(login_request: Login, session: SessionDep):
    user = session.exec(select(User).where(User.email == login_request.email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User does not exist")
    if not verify_pass(login_request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": str(user.uuid)})
    refresh_token = create_refresh_token({"sub": str(user.uuid)})

    return {"access_token": access_token, "refresh_token": refresh_token}

@app.post("/refresh/")
async def refresh_token(uuid: str = Depends(authorize_refresh)):    
    access_token = create_access_token({"sub": uuid})
    return {"access_token": access_token}

@app.get("/user/")
async def get_user(session: SessionDep, uuid: str = Depends(authorize_request)):
    statement = select(User).where(User.uuid == uuid)
    user = session.exec(statement).first()

    return {"user": {"id": user.uuid,"email": user.email, "verified": user.verified}}
