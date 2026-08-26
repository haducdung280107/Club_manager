from db.database import Base
from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class ClubsModel(Base):
    __tablename__="clubs"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50),nullable=False)
    description=Column(Text,nullable=True)
    owner_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at=Column(DateTime, nullable=False,default=datetime.utcnow)

    owner=relationship("UsersModel",back_populates="clubs")
    club_members = relationship("Club_Members_Model", back_populates="clubs")
    activities = relationship("Club_Activities_Model", back_populates="clubs")