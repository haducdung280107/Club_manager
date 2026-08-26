from db.database import Base
from sqlalchemy import Column,Integer,DateTime,ForeignKey,Enum,String,Text
from datetime import datetime
from sqlalchemy.orm import relationship

class Club_Activities_Model(Base):
    __tablename__="club_activities"

    id=Column(Integer,primary_key=True,index=True)
    club_id=Column(Integer,ForeignKey("clubs.id"),nullable=False)
    title=Column(String(50),nullable=False)
    description=Column(Text,nullable=True)
    assignee_id=Column(Integer,ForeignKey("users.id"),nullable=True)
    status = Column(Enum("TODO", "IN_PROGRESS", "DONE"), nullable=False, default="TODO")
    priority = Column(Enum("LOW", "MEDIUM", "HIGH"), nullable=False, default="MEDIUM")
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    clubs = relationship("ClubsModel", back_populates="activities")
    assignee = relationship("UsersModel", back_populates="activities")