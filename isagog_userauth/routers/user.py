""" implement all user management routes
login and refresh are open to all
the rest need an admin user
"""

from datetime import timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..config import ACCESS_TOKEN_LIFETIME, JWT_SECRET
from ..db_session import get_db
from ..models import User
from ..schemas import (
    DeleteUserModel,
    SignupModel,
    SignupResponseModel,
    PasswordChangeModel,
)
from ..utils import (
    create_access_token,
    create_refresh_token,
    get_admin_user,
    get_current_user,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix="/user")


@router.post(
    "/signup",
    response_model=SignupResponseModel,
    dependencies=[Depends(get_admin_user)],
)
def save_user(user: SignupModel, db: Session = Depends(get_db)):
    """an admin protected route to register a new user"""
    existing_user_by_email = db.query(User).filter(User.email == user.email).first()
    if existing_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_user_by_username = (
        db.query(User).filter(User.username == user.username).first()
    )
    if existing_user_by_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    if user.role not in ["admin", "basic"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return SignupResponseModel(
        email=db_user.email, username=db_user.username, role=db_user.role
    )


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """a login route for all users; will return valid JWT tokens when successful"""
    user = (
        db.query(User)
        .filter(
            or_(User.email == form_data.username, User.username == form_data.username)
        )
        .first()
    )
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401, detail="Invalid email/username or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_LIFETIME)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id, "role": user.role},
        expires_delta=access_token_expires,
    )
    new_refresh_token = create_refresh_token(data={"sub": user.email, "id": user.id})
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "role": user.role,  # Include role in response
    }


@router.post("/refresh")
async def refresh_token(request: Request, db: Session = Depends(get_db)):
    """refresh an access token"""
    refresh_token_value = (await request.json()).get("refresh_token")
    try:
        payload = jwt.decode(refresh_token_value, JWT_SECRET, algorithms=["HS256"])
        user = db.query(User).filter(User.email == payload["sub"]).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        new_access_token = create_access_token(data={"sub": user.email, "id": user.id})
        return {"access_token": new_access_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=401, detail="Refresh token has expired"
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


@router.get("/list", dependencies=[Depends(get_admin_user)])
def list_users(db: Session = Depends(get_db)):
    """admins can list defined users"""
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role,
        }
        for user in users
    ]


@router.delete("/delete", dependencies=[Depends(get_admin_user)])
def delete_user(user_data: DeleteUserModel, db: Session = Depends(get_db)):
    """admins can delete a user using the numeric ID"""
    user = db.query(User).filter(User.id == user_data.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.put("/passchange")
def change_user_password(
    user_update: PasswordChangeModel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change the password; admins can change any, basic users only theirs"""
    if current_user.role != "admin" and current_user.email != user_update.email:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user = db.query(User).filter(User.email == user_update.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = get_password_hash(user_update.new_password)
    db.commit()
    return {"message": "Password updated successfully"}
