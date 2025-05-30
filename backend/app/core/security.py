from datetime import datetime, timedelta, timezone
from typing import Optional, Any

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request # Added Request
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.schemas.token import TokenData
from app.models.user import User
from app.crud.crud_user import user as crud_user
from app.db.session import get_db
from sqlalchemy.orm import Session


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme (primarily for API documentation and potential future use with Bearer tokens)
# Actual token retrieval for web app will be from HttpOnly cookie.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.SERVER_HOST}/api/v1/auth/token") # Example token URL

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user_from_cookie(
    request: Request, # Use fastapi.Request
    db: Session = Depends(get_db)
) -> Optional[User]:
    token = request.cookies.get(settings.JWT_COOKIE_NAME)
    if not token:
        return None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            # Consider logging this invalid token event
            return None
        # No need to create TokenData object here if only email is used from payload for DB lookup
    except JWTError: # Catches expired signature, invalid signature, etc.
        # Consider logging this event
        return None

    db_user = crud_user.get_user_by_email(db, email=email) # Use the extracted email directly
    if db_user is None:
        # User from token not found in DB (e.g., deleted after token issuance)
        return None
    return db_user


async def get_current_active_user(
    current_user: Optional[User] = Depends(get_current_user_from_cookie) # Changed to Optional[User]
) -> User: # Still returns User, but raises error if not found or inactive
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}, # Though we use cookies, this is standard for 401
        )
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user
