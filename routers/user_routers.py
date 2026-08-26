from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.users_schema import UserRespone
from dependencies.auth import get_current_user,require_role
from services.user_services import get_users_list
from typing import Optional
import models
router=APIRouter(prefix="/users",tags=["Users"])

@router.get("/me",response_model=UserRespone)
def get_user(current_user=Depends(get_current_user)):
    return current_user
@router.get("/", response_model=list[UserRespone])
def read_users(
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin_user: models.users.UsersModel = Depends(require_role(["ADMIN"]))
):
    return get_users_list(db=db, search=search, is_active=is_active)