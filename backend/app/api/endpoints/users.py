from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.models.user import User as DBUser # Alias to avoid confusion with Pydantic schema
from app.schemas.user import User as UserSchema # Pydantic schema for returning user info

router = APIRouter()

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: DBUser = Depends(get_current_active_user)):
    """
    Fetch the current logged in user.
    """
    if not current_user:
        # This case should ideally be handled by get_current_active_user dependency raising 401
        raise HTTPException(status_code=404, detail="User not found")
    return current_user
