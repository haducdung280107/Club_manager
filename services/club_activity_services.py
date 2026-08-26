from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from fastapi import HTTPException, status
import math
from models.clubs import ClubsModel
from models.club_members import Club_Members_Model
from models.club_activities import Club_Activities_Model
from core.exceptions import forbidden
from schemas.club_activity_schema import ActivityCreateRequest, ActivityUpdateRequest, ActivityStatus, ActivityPriority

# 1. Hàm kiểm tra thành viên 
def check_club_membership(club_id: int, user_id: int, db: Session):
    club = db.query(ClubsModel).filter(ClubsModel.id == club_id).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy câu lạc bộ")
    
    member = db.query(Club_Members_Model).filter(Club_Members_Model.club_id == club_id,Club_Members_Model.user_id == user_id).first()
    
    if not member:
        raise forbidden("Bạn không phải thành viên của câu lạc bộ này")
    return member  

# 2. Hàm tạo hoạt động mới
def create_activity(club_id: int, request: ActivityCreateRequest, db: Session, current_user):
    check_club_membership(club_id, current_user.id, db)

    new_activity = Club_Activities_Model(
    club_id=club_id,
    title=request.title,
    description=request.description,
    priority=request.priority,
    due_date=request.due_date
)
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

# 3. Hàm lấy danh sách hoạt động (Search, Filter, Phân trang, Sắp xếp)
def get_club_activities(
    club_id: int, 
    db: Session, 
    current_user,
    search: str | None = None,
    status_filter: ActivityStatus | None = None,
    priority_filter: ActivityPriority | None = None,
    assignee_id: int | None = None,
    page: int = 1,
    size: int = 10,
    sort_by: str = "created_at",
    order: str = "desc"
):
    check_club_membership(club_id, current_user.id, db)
    query = db.query(Club_Activities_Model).filter(Club_Activities_Model.club_id == club_id)
    # Lọc điều kiện
    if search:
        query = query.filter(Club_Activities_Model.title.ilike(f"%{search}%"))
    if status_filter:
        query = query.filter(Club_Activities_Model.status == status_filter.value)
    if priority_filter:
        query = query.filter(Club_Activities_Model.priority == priority_filter.value)
    if assignee_id is not None:
        query = query.filter(Club_Activities_Model.assignee_id == assignee_id)
    # Đếm tổng số bản ghi thỏa điều kiện
    total = query.count()
    # Sắp xếp theo created_at hoặc due_date
    sort_column = getattr(Club_Activities_Model, sort_by if sort_by in ["created_at", "due_date"] else "created_at")
    if order.lower() == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    # Phân trang
    offset = (page - 1) * size
    activities = query.offset(offset).limit(size).all()
    total_pages = math.ceil(total / size) if total > 0 else 0
    return {
        "items": activities,
        "total": total,
        "page": page,
        "size": size,
        "total_pages": total_pages
    }
# 4. Hàm lấy chi tiết 1 hoạt động
def get_activity_detail(activity_id: int, db: Session, current_user):
    activity = db.query(Club_Activities_Model).filter(Club_Activities_Model.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy hoạt động")
    check_club_membership(activity.club_id, current_user.id, db)
    return activity
# 5. Hàm cập nhật hoạt động 
def update_activity_detail(activity_id: int, request: ActivityUpdateRequest, db: Session, current_user):
    activity = db.query(Club_Activities_Model).filter(Club_Activities_Model.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy hoạt động")

    member = check_club_membership(activity.club_id, current_user.id, db)

    is_owner = (member.role == "OWNER")
    is_creator = (activity.created_by == current_user.id)
    is_assignee = (activity.assignee_id == current_user.id)

    if not (is_owner or is_assignee):
        raise forbidden("Bạn không có quyền chỉnh sửa hoạt động này")
    update_data = request.model_dump(exclude_unset=True)

    if is_assignee and not (is_owner or is_creator):
        forbidden_fields = {"title", "description", "due_date", "priority", "assignee_id"}
        if any(f in update_data for f in forbidden_fields):
            raise forbidden("Người được giao việc chỉ được phép cập nhật trạng thái (status)")

    if "assignee_id" in update_data and update_data["assignee_id"] is not None:
        assignee_member = db.query(Club_Members_Model).filter(
            Club_Members_Model.club_id == activity.club_id,Club_Members_Model.user_id == update_data["assignee_id"]).first()
        if not assignee_member:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Người được giao việc (assignee) không phải thành viên trong câu lạc bộ")

    for field, value in update_data.items():
        setattr(activity, field, value)

    db.commit()
    db.refresh(activity)
    return activity

# 6. Hàm xóa hoạt động
def delete_activity_detail(activity_id: int, db: Session, current_user):
    activity = db.query(Club_Activities_Model).filter(Club_Activities_Model.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy hoạt động")
    user_member = check_club_membership(activity.club_id, current_user.id, db)
    if user_member.role != "OWNER" and activity.created_by != current_user.id:
        raise forbidden("Chỉ OWNER câu lạc bộ hoặc người tạo hoạt động mới có quyền xóa")

    db.delete(activity)
    db.commit()
    return {"message": "Đã xóa hoạt động thành công"}