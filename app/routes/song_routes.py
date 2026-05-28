import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlmodel import Session
from app.db.database import get_session
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from app.core.config import settings
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/song", tags=["Upload Song"])

cloudinary.config(
    cloud_name="dkhsttchv",
    api_key="246684925226145",
    api_secret=settings.CLOUDINARY_API_KEY,
    secure=True,
)


@router.post("/upload")
def upload_song(
    song_audio: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    artist: str = Form(...),
    song_name: str = Form(...),
    hex_code: str = Form(...),
    db: Session = Depends(get_session),
    auth_user: dict = Depends(get_current_user),
):
    song_id = str(uuid.uuid4())
    song_upload_response = cloudinary.uploader.upload(
        song_audio.file, resource_type="auto", folder=f"songs/{song_id}"
    )
    thumnail_upload_response = cloudinary.uploader.upload(
        thumbnail.file, resource_type="image", folder=f"songs/{song_id}"
    )
