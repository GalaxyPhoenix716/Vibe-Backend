from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    name: str

    email: str = Field(unique=True, index=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
