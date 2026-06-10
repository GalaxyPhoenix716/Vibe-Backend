from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from app.schemas.song import SongResponse

class PlaylistCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    thumbnail_url: Optional[str] = Field(default=None, max_length=512)


class AddPlaylistSong(BaseModel):
    playlist_id: UUID
    song_id: str


class PlaylistResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PlaylistWithSongsResponse(PlaylistResponse):
    songs: List[SongResponse] = []

    model_config = {"from_attributes": True}
