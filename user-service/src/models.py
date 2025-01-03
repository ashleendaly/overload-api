from sqlmodel import Field, SQLModel
import uuid as uuid_pkg

class User(SQLModel, table=True):
    uuid: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    email: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(nullable=False)
    verified: bool = Field(default=False, nullable=False)