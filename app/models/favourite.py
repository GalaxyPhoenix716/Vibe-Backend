from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID


class Favourites(SQLModel, table=True):
    __tablename__ = "favourites"

    id: str = Field(primary_key=True, index=True)

    song_id: str = Field(foreign_key="songs.id")

    user_id: UUID = Field(foreign_key="users.id")

    song: "Song" = Relationship()
    user: "User" = Relationship(back_populates="favourites")
