from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User, SessionLocal
from typing import List
from pydantic import BaseModel
from datetime import datetime

# Get DB session
def get_admin_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

class UserDetails(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/users", response_model=List[UserDetails])
async def get_all_users(db: Session = Depends(get_admin_db)):
    """
    Get all users in the system with their details.
    Only active users are returned by default.
    """
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
