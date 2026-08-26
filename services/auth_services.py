from models.users import UsersModel
from schemas.users_schema import UserCreateRequest,LoginRequest,LoginRespone
from sqlalchemy.orm import Session
from core.security import hash_password,verify_password,create_access_token
from core.exceptions import bad_request

# Đăng ký tài khoản
def register_user(request:UserCreateRequest,db:Session):
    user_db=db.query(UsersModel).filter(UsersModel.email==request.email).first()
    if user_db:
        raise bad_request("Email đã tồn tại")
    hashed_password = hash_password(request.password)

    new_user = UsersModel(
        email = request.email , 
        password_hash = hashed_password , 
        full_name = request.full_name,
        role = "USER" , 
        is_active=True 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
# Đăng nhập tài khoản
def login_user(request:LoginRequest,db:Session) -> LoginRespone:
    user=db.query(UsersModel).filter(UsersModel.email==request.email).first()
    if not user:
        raise bad_request("Email hoặc mật khẩu không chính xác")
    if not verify_password(request.password,user.password_hash):
        raise bad_request("Email hoặc mật khẩu không chính xác")
    if not user.is_active:
        raise bad_request("Tài khoản của bạn đã bị khóa")
    access_token=create_access_token(data={"sub":str(user.id),"email":user.email,"role":user.role})
    return LoginRespone(access_token=access_token,token_type="bearer")
