from fastapi import APIRouter

router = APIRouter(prefix='/song', tags=["Upload Song"])

@router.post('/upload')
def upload_song() :
    pass