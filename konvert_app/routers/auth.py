import uuid
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from konvert_app.core.database import SessionLocal
from konvert_app.models.user import User
from konvert_app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from konvert_app.services.email_service import send_verification_email

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        raise HTTPException(400, "Email and password required")

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email already registered")

    token = str(uuid.uuid4())

    user = User(
        email=email,
        password_hash=hash_password(password),
        is_verified=False,
        verification_token=token,
    )
    db.add(user)
    db.commit()

    verify_url = f"{os.getenv('BASE_URL')}/auth/verify-email?token={token}"
    send_verification_email(email, token)

    return {"message": "Verification email sent"}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user.is_verified = True
    user.verification_token = None
    db.commit()

    access_token = create_access_token({"sub": str(user.id)})

    return {
        "message": "Email verified successfully",
        "access_token": access_token,
        "token_type": "bearer",
    }



@router.post("/login")
def login(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")

    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "EMAIL_NOT_VERIFIED",
                "message": "Email not verified"
            }
        )

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}

@router.post("/resend-verification")
def resend_verification(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email")

    if not email:
        raise HTTPException(status_code=400, detail="Email required")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email already verified"}

    if not user.verification_token:
        user.verification_token = str(uuid.uuid4())
        db.commit()

    verify_url = f"{os.getenv('BASE_URL')}/auth/verify-email?token={user.verification_token}"
    send_verification_email(user.email, user.verification_token)

    return {"message": "Verification email sent"}

