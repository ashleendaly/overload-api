from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    username: str = Field(default=None, primary_key=True)
    password: str = Field(default=None)
    email: str = Field(index=True)