from fastapi import Header, HTTPException, Depends
from sqlmodel import Session, select
from app.auth.jwt_handler import verify_token
from app.db.database import get_session
from app.models.user import User
from uuid import UUID


def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_session),
):
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format",
        )

    token = authorization.split(" ")[1]
    payload = verify_token(token)
    
    sub = payload.get("sub")
    email = payload.get("email")
    name = payload.get("user_metadata", {}).get("full_name", "User")
    
    if not sub or not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Ensure user exists in db and has correct UUID
    user = db.exec(select(User).where(User.id == sub)).first()
    if not user:
        user_by_email = db.exec(select(User).where(User.email == email)).first()
        if user_by_email:
            user_by_email.id = UUID(sub)
            db.add(user_by_email)
            db.commit()
            db.refresh(user_by_email)
        else:
            new_user = User(id=UUID(sub), name=name, email=email)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

    return {
        "id": sub,
        "email": email,
    }
