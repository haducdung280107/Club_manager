from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.users import UsersModel

def get_users_list(
    db: Session, 
    search: Optional[str] = None, 
    is_active: Optional[bool] = None
) -> list[UsersModel]:
    query = db.query(UsersModel)

    # Filter theo trạng thái hoạt động nếu có truyền parameter
    if is_active is not None:
        query = query.filter(UsersModel.is_active == is_active)

    # Tìm kiếm gần đúng theo Name hoặc Email nếu có truyền từ khóa
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                UsersModel.full_name.ilike(search_pattern),
                UsersModel.email.ilike(search_pattern)
            )
        )

    return query.all()