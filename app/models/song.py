from typing import List
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4
from datetime import datetime, UTC
from app.models.playlist import Playlist, PlaylistSongLink

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
    
    tags: str

    playlists: List[Playlist] = Relationship(
        back_populates="songs",
        link_model=PlaylistSongLink
    )
