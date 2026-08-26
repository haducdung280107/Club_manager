from pydantic import BaseModel , EmailStr , Field , ConfigDict
from datetime import datetime 

class UserCreateRequest(BaseModel):  # schema nhận dữ liệu từ người dùng gửi lên 
    email : EmailStr 
    full_name : str = Field(min_length=2,max_length=100)
    password : str = Field(min_length=6,max_length=100)

class UserUpdateRequest(BaseModel): 
    full_name : str | None = Field(default=None , min_length=2 , max_length=100)
    is_active: bool | None = None

class UserRespone(BaseModel): 
    id : int 
    email : str 
    full_name : str
    role : str 
    is_active : bool
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel): 
    email: EmailStr
    password : str 

class LoginRespone(BaseModel): 
    access_token : str 
    token_type : str

