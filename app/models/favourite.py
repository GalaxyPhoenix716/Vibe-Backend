from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from uuid import UUID
from app.models.song import Song


class Favourite(SQLModel, table=True):
    __tablename__ = "favourites"
    __table_args__ = (UniqueConstraint("user_id", "song_id", name="uq_user_song_favourite"),)

    id: str = Field(primary_key=True, index=True)

    song_id: str = Field(foreign_key="songs.id")

    user_id: UUID = Field(foreign_key="users.id")

    song: "Song" = Relationship()
    user: "User" = Relationship(back_populates="favourites")
