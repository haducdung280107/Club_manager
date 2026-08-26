from fastapi import APIRouter,status,Depends
from db.database import get_db
from dependencies.auth import get_current_user
from schemas.clubs_schema import *
from schemas.club_members_schema import ClubMemberCreateRequest
from sqlalchemy.orm import Session
from services.club_services import create_club,get_my_club,get_club_by_id,update_club,delete_club,add_member_club,remove_member_club,get_club_members
from schemas.club_members_schema import ClubMemberResponse
router=APIRouter(prefix="/clubs", tags=["Clubs"])

@router.post("/",response_model=ClubResponse,status_code=status.HTTP_201_CREATED)
def create_new_club(request:ClubCreateRequest,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return create_club(request=request,db=db,current_user=current_user)

@router.get("/",response_model=list[ClubResponse],status_code=status.HTTP_200_OK)
def get_club(search:str |None=None,current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_my_club(search=search,current_user=current_user,db=db)

@router.get("/{club_id}",response_model=ClubResponse,status_code=status.HTTP_200_OK)
def get_club_id(club_id:int,current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_club_by_id(club_id=club_id,current_user=current_user,db=db)

@router.put("/{club_id}", response_model=ClubResponse,status_code=status.HTTP_200_OK)
def update_existing_club(club_id: int,request: ClubUpdateRequest,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return update_club(club_id=club_id, request=request, db=db, current_user=current_user)

@router.delete("/{club_id}",status_code=status.HTTP_200_OK)
def delete_existing_club(club_id: int,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return delete_club(club_id=club_id, db=db, current_user=current_user)

@router.post("/{club_id}/members", response_model=ClubMemberResponse, status_code=status.HTTP_201_CREATED)
def add_member(club_id: int, request: ClubMemberCreateRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return add_member_club(club_id=club_id, request=request, db=db, current_user=current_user)

@router.delete("/{club_id}/members/{user_id}",status_code=status.HTTP_200_OK)
def remove_member(club_id: int, user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return remove_member_club(club_id=club_id, target_user_id=user_id, db=db, current_user=current_user)

@router.get("/{club_id}/members", response_model=list[ClubMemberResponse],status_code=status.HTTP_200_OK)
def list_members(club_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_club_members(club_id=club_id, db=db, current_user=current_user)