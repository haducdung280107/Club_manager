from db.database import Base
from sqlalchemy import Column,Integer,String ,DateTime,Boolean,Enum
from datetime import datetime
from sqlalchemy.orm import relationship

class UsersModel(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    email=Column(String(50),unique=True,nullable=False)
    password_hash=Column(String(255),nullable=False)
    full_name=Column(String(50),nullable=False)
    role=Column(Enum("USER","ADMIN"),nullable=False,default="USER")
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime, nullable=False,default=datetime.utcnow)

    clubs=relationship("ClubsModel",back_populates="owner")
    club_members=relationship("Club_Members_Model",back_populates="users")
    activities = relationship("Club_Activities_Model", back_populates="assignee")