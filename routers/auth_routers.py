from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.users_schema import UserCreateRequest, UserRespone , LoginRequest, LoginRespone
from services.auth_services import register_user,login_user

router=APIRouter()

@router.post("/register",response_model=UserRespone)
def register(request:UserCreateRequest,db:Session=Depends(get_db)):
    return register_user(request=request,db=db)
@router.post("/login",response_model=LoginRespone)
def login(request:LoginRequest,db:Session=Depends(get_db)):
    return login_user(request=request,db=db)
