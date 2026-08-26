from fastapi import FastAPI,Depends
from db.database import Base,engine,get_db
from sqlalchemy.orm import Session

from models.users import UsersModel
from models.clubs import ClubsModel
from models.club_members import Club_Members_Model
from models.club_activities import Club_Activities_Model
from routers import auth_routers,user_routers,club_routers,club_activity_routers

Base.metadata.create_all(bind=engine)
app=FastAPI()

app.include_router(auth_routers.router)
app.include_router(user_routers.router)
app.include_router(club_routers.router)
app.include_router(club_activity_routers.router)

@app.get("/health")
def health_check(db : Session = Depends(get_db)):
    return {"status": "healthy", "database": "connected"}

@app.get("/")
def home():
    return {"message": "Chào mừng đến với API Quản lý Câu lạc bộ!"}