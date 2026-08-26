from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from dependencies.auth import get_current_user
from schemas.club_activity_schema import ActivityCreateRequest, ActivityResponse,ActivityUpdateRequest,PaginatedActivityResponse,ActivityStatus,ActivityPriority
from services.club_activity_services import create_activity, get_club_activities, get_activity_detail,update_activity_detail,delete_activity_detail

router = APIRouter(tags=["Club Activities"])

@router.post("/clubs/{club_id}/activities", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_new_activity(club_id: int,request: ActivityCreateRequest,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return create_activity(club_id=club_id, request=request, db=db, current_user=current_user)

@router.get("/activities/{activity_id}", response_model=ActivityResponse)
def get_activity_by_id(activity_id: int,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return get_activity_detail(activity_id=activity_id, db=db, current_user=current_user)

@router.patch("/activities/{activity_id}", response_model=ActivityResponse)
def patch_activity(activity_id: int,request: ActivityUpdateRequest,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return update_activity_detail(activity_id=activity_id, request=request, db=db, current_user=current_user)

@router.delete("/activities/{activity_id}")
def delete_activity(activity_id: int,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return delete_activity_detail(activity_id=activity_id, db=db, current_user=current_user)

@router.get("/clubs/{club_id}/activities", response_model=PaginatedActivityResponse)
def list_club_activities(
    club_id: int,
    search: str | None = None,
    status_filter: ActivityStatus | None = None,
    priority_filter: ActivityPriority | None = None,
    assignee_id: int | None = None,
    page: int = 1,
    size: int = 10,
    sort_by: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_club_activities(
        club_id=club_id, db=db, current_user=current_user,
        search=search, status_filter=status_filter, priority_filter=priority_filter,
        assignee_id=assignee_id, page=page, size=size, sort_by=sort_by, order=order
    )
