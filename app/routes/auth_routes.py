from fastapi import APIRouter, Header, Depends, HTTPException
from sqlmodel import Session, select
from app.db.database import get_session
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
