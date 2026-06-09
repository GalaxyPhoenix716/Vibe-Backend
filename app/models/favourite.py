from pydantic import Field
from sqlmodel import ForeignKey, SQLModel


class Favourites(SQLModel, table=True):
    __tablename__ = "favourites"

    id: str = Field(primary_key=True, index=True)

    song_id: str = Field(ForeignKey("songs.id"))

    user_id: str = Field(ForeignKey("users.id"))
