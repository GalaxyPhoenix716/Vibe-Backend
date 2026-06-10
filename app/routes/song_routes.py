import uuid
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from app.db.database import get_session
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from app.core.config import settings
from app.middleware.auth_middleware import get_current_user
from app.models.favourite import Favourites
from app.schemas.favourite import FavouriteSong
from app.models.song import Song

router = APIRouter(prefix="/song", tags=["Upload Song"])

cloudinary.config(
    cloud_name="dkhsttchv",
    api_key="246684925226145",
    api_secret=settings.CLOUDINARY_API_KEY,
    secure=True,
)


@router.post("/upload", status_code=201)
def upload_song(
    song_audio: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    artist: str = Form(...),
    song_name: str = Form(...),
    tags: str = Form(...),
    db: Session = Depends(get_session),
    auth_user: dict = Depends(get_current_user),
):
    song_id = str(uuid.uuid4())
    song_upload_response = cloudinary.uploader.upload(
        song_audio.file, resource_type="auto", folder=f"songs/{song_id}"
    )
    thumbnail_upload_response = cloudinary.uploader.upload(
        thumbnail.file, resource_type="image", folder=f"songs/{song_id}"
    )

    new_song = Song(
        id=song_id,
        song_name=song_name,
        artist=artist,
        tags=tags,
        song_url=song_upload_response["url"],
        thumbnail_url=thumbnail_upload_response["url"],
    )

    db.add(new_song)
    db.commit()
    db.refresh(new_song)

    return {
        "message": "Song uploaded successfully",
        "song": {
            "id": new_song.id,
            "song_name": new_song.song_name,
            "artist": new_song.artist,
            "song_url": new_song.song_url,
            "thumbnail_url": new_song.thumbnail_url,
            "tags": new_song.tags,
        },
    }


@router.get("/list", status_code=200)
def fetchSongs(
    db: Session = Depends(get_session), auth_details=Depends(get_current_user)
):
    songs = db.query(Song).all()
    return songs


@router.post("/favourite", status_code=201)
def favouriteSong(
    fav_song: FavouriteSong,
    db: Session = Depends(get_session),
    auth_details=Depends(get_current_user),
):
    user_id = auth_details["id"]

    fav_song_res = (
        db.query(Favourites)
        .filter(Favourites.song_id == fav_song.song_id, Favourites.user_id == user_id)
        .first()
    )

    if fav_song_res:
        db.delete(fav_song_res)
        db.commit()

        return {"message": False}
    else:
        new_fav = Favourites(id=str(uuid.uuid4()), song_id=fav_song.song_id, user_id=user_id)
        db.add(new_fav)
        db.commit()
        return {"message": True}


@router.get("/list-favourites", status_code=200)
def fetchFavSongs(
    db: Session = Depends(get_session), auth_details=Depends(get_current_user)
):
    user_id = auth_details["id"]
    fav_songs = (
        db.query(Favourites)
        .filter(Favourites.user_id == user_id)
        .options(joinedload(Favourites.song))
        .all()
    )
    return fav_songs
