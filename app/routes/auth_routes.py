from fastapi import APIRouter, Header, Depends, HTTPException
from sqlmodel import Session, select
from app.db.database import get_session
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.auth.jwt_handler import verify_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def google_auth(authorization: str = Header(), session: Session = Depends(get_session)):

    try:
        token = authorization.split(" ")[1]

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    payload = verify_token(token)
    email = payload["email"]
    name = payload.get("user_metadata", {}).get("full_name", "User")
    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        user = User(name=name, email=email)

        session.add(user)
        session.commit()
        session.refresh(user)

    return {
        "message": "Authentication successful",
        "user": {"id": str(user.id), "name": user.name, "email": user.email},
    }


@router.get("/")
def current_user_data(
    db: Session = Depends(get_session), user_dict=Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_dict["id"]).first()

    if not user:
        raise HTTPException(404, "User not found!")

    return user
