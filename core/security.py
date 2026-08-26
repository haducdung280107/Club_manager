import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES , REFRESH_TOKEN_EXPIRE_DAYS

# băm mật khẩu
def hash_password(password:str):
    salt=bcrypt.gensalt()

    hashed=bcrypt.hashpw(password.encode("utf-8"),salt)

    return hashed.decode("utf-8")

# kiểm tra mật khẩu
def verify_password(plain_password:str,hashed_password:str):

    return bcrypt.checkpw(plain_password.encode("utf-8"),hashed_password.encode("utf-8"))

# tạo token
def create_access_token(data:dict):
    tokens=data.copy()

    expire=datetime.now(timezone.utc)+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    tokens.update({"exp":expire})

    encoded_jwt=jwt.encode(tokens,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
