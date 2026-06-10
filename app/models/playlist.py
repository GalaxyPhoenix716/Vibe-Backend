import uuid
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship

class PlaylistSongLink(SQLModel, table=True):
    __tablename__ = "playlist_songs"

    id: UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    playlist_id: UUID = Field(
        foreign_key="playlists.id",
        nullable=False
    )
    song_id: str = Field(
        foreign_key="songs.id", 
        nullable=False
    )
    added_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )


class PlaylistBase(SQLModel):
    name: str = Field(max_length=255, index=True)
    description: Optional[str] = None
    thumbnail_url: Optional[str] = Field(default=None, max_length=512)


class Playlist(PlaylistBase, table=True):
    __tablename__ = "playlists"

    id: UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    user_id: UUID = Field(
        foreign_key="users.id", 
        nullable=False
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

    # Relationships
    songs: List["Song"] = Relationship(
        back_populates="playlists", 
        link_model=PlaylistSongLink
    )
