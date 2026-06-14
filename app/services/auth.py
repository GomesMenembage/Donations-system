from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.security import create_access_token, hash_password, verify_password


def register_user(db: Session, name: str, email: str, password: str, location: str | None, role: str) -> User:
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise ValueError("Email already registered")

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        location=location,
        role=role,
        status="active" if role == "donor" else "pending",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password")
    if user.status != "active":
        raise ValueError("Account is not active")
    return user


def login(db: Session, email: str, password: str) -> dict:
    user = authenticate_user(db, email, password)
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


def request_password_reset(db: Session, email: str) -> str | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    token = create_access_token({"sub": str(user.id), "reset": True}, expires_delta=timedelta(minutes=30))
    return token


def reset_password(db: Session, token: str, new_password: str) -> User:
    from app.utils.security import decode_access_token

    payload = decode_access_token(token)
    if not payload or not payload.get("reset"):
        raise ValueError("Invalid or expired reset token")

    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise ValueError("User not found")

    user.password_hash = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user
