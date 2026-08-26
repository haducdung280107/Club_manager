from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ClubMemberCreateRequest(BaseModel):  # schema nhận dữ liệu thêm thành viên
    user_id: int


class ClubMemberResponse(BaseModel):  # schema trả thông tin thành viên
    id: int
    club_id: int
    user_id: int
    role: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)