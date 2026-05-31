from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime, UTC

class Song(SQLModel, table=True):

    __tablename__ = "songs"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
    )

    song_name: str

    artist: str

    song_url: str

    thumbnail_url: str
    
    tags: list[str]
