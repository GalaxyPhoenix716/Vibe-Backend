from pydantic import Field
from sqlmodel import ForeignKey, SQLModel
from sqlalchemy.orm import relationship


class Favourites(SQLModel, table=True):
    __tablename__ = "favourites"

    id: str = Field(primary_key=True, index=True)

    song_id: str = Field(ForeignKey("songs.id"))

    user_id: str = Field(ForeignKey("users.id"))

    song = relationship("Song")
    user = relationship("Users", back_populates="favourites")
