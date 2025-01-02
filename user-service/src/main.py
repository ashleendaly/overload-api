from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import select

from src.models import User 
from src.auth import hash_pass, verify_pass
from src.db import create_db_and_tables, SessionDep

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return "Active"

class Register(BaseModel):
    username: str
    password: str
    email: str

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
async def login(user: Login, session: SessionDep):
    u = session.exec(select(User).where(User.username == user.username)).one()
    if verify_pass(user.password, u.password):
        return "Success"
    return "Failed"