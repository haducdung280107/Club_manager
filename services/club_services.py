from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.clubs import ClubsModel
from models.club_members import Club_Members_Model
from models.users import UsersModel
from schemas.clubs_schema import ClubCreateRequest, ClubUpdateRequest
from schemas.club_members_schema import ClubMemberCreateRequest
from core.exceptions import forbidden 

# Hàm kiểm tra quyền OWNER
def check_club_owner(club_id: int, user_id: int, db: Session):
    club = db.query(ClubsModel).filter(ClubsModel.id == club_id).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy câu lạc bộ")
    
    if club.owner_id != user_id:
        raise forbidden("Chỉ OWNER mới có quyền thực hiện thao tác này")
    return club

# Tạo club mới 
def create_club(request: ClubCreateRequest, db: Session, current_user):
    new_club = ClubsModel(
        name=request.name,
        description=request.description,
        owner_id=current_user.id
    )
    db.add(new_club)
    db.flush()

    new_member = Club_Members_Model(
        club_id=new_club.id,
        user_id=current_user.id,
        role="OWNER"
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_club)
    return new_club

# Lấy dữ liệu các câu lạc bộ của tôi
def get_my_club(current_user, db: Session, search: str | None = None):
    query = db.query(ClubsModel).join(
        Club_Members_Model, Club_Members_Model.club_id == ClubsModel.id
    ).filter(Club_Members_Model.user_id == current_user.id)

    if search:
        query = query.filter(ClubsModel.name.contains(search))
    return query.all()

# Lấy chi tiết câu lạc bộ 
def get_club_by_id(club_id: int, db: Session, current_user):
    club = db.query(ClubsModel).filter(ClubsModel.id == club_id).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy club")
    
    member = db.query(Club_Members_Model).filter(
        Club_Members_Model.club_id == club_id,
        Club_Members_Model.user_id == current_user.id
    ).first()
    
    if not member:
        raise forbidden("Bạn không phải thành viên câu lạc bộ")
    return club

# Cập nhật câu lạc bộ 
def update_club(club_id: int, request: ClubUpdateRequest, db: Session, current_user):
    club = check_club_owner(club_id, current_user.id, db)
    
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(club, key, value)

    db.commit()
    db.refresh(club)
    return club

# Xoá câu lạc bộ 
def delete_club(club_id: int, db: Session, current_user):
    club = check_club_owner(club_id, current_user.id, db)
    db.query(Club_Members_Model).filter(Club_Members_Model.club_id == club_id).delete()

    db.delete(club)
    db.commit()
    return {"message": "Đã xoá câu lạc bộ thành công"}

# Thêm thành viên
def add_member_club(club_id: int, request: ClubMemberCreateRequest, db: Session, current_user):
    check_club_owner(club_id, current_user.id, db)
    
    target_user = db.query(UsersModel).filter(UsersModel.id == request.user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
    
    existing_member = db.query(Club_Members_Model).filter(
        Club_Members_Model.club_id == club_id,
        Club_Members_Model.user_id == request.user_id
    ).first()
    if existing_member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Thành viên đã ở trong câu lạc bộ")

    new_member = Club_Members_Model(
        club_id=club_id,
        user_id=request.user_id,
        role="MEMBER"
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

# Xoá thành viên
def remove_member_club(club_id: int, target_user_id: int, db: Session, current_user):
    check_club_owner(club_id, current_user.id, db)
    
    member = db.query(Club_Members_Model).filter(
        Club_Members_Model.club_id == club_id,
        Club_Members_Model.user_id == target_user_id
    ).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thành viên không thuộc câu lạc bộ này")

    if member.role == "OWNER":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể xóa OWNER khỏi câu lạc bộ")

    db.delete(member)
    db.commit()
    return {"message": "Đã xóa thành viên khỏi câu lạc bộ"}

# Lấy danh sách thành viên
def get_club_members(club_id: int, db: Session, current_user):
    club = db.query(ClubsModel).filter(ClubsModel.id == club_id).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy câu lạc bộ")
    
    return db.query(Club_Members_Model).filter(Club_Members_Model.club_id == club_id).all()