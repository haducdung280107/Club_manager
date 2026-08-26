from db.database import Base
from sqlalchemy import Column,Integer,DateTime,ForeignKey,Enum
from datetime import datetime
from sqlalchemy.orm import relationship

class Club_Members_Model(Base):
    __tablename__="club_members"

    club_id=Column(Integer,ForeignKey("clubs.id"),primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"),primary_key=True)
    role=Column(Enum("OWNER","MEMBER"),nullable=False)
    joined_at=Column(DateTime, nullable=False,default=datetime.utcnow)

    users=relationship("UsersModel",back_populates="club_members")
    clubs = relationship("ClubsModel", back_populates="club_members")