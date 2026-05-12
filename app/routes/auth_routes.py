from fastapi import APIRouter, Header, Depends, HTTPException
from sqlmodel import Session, select

from db.database import get_session
from auth.auth import verify_token
from models.user import User

router = APIRouter()


@router.post("/auth/login")
def login(authorization: str = Header(None), session: Session = Depends(get_session)):

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.split(" ")[1]

    payload = verify_token(token)

    email = payload["email"]

    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        user = User(
            name=payload.get("user_metadata", {}).get("full_name", "User"), email=email
        )

        session.add(user)
        session.commit()
        session.refresh(user)

    return {"id": str(user.id), "name": user.name, "email": user.email}
