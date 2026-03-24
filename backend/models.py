from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum


class PriorityLevel(str, enum.Enum):
    low    = "low"
    medium = "medium"
    high   = "high"


class Course(Base):
    __tablename__ = "courses"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(120), nullable=False)
    days       = Column(String(30),  nullable=False)
    start_time = Column(String(5),   nullable=False)
    end_time   = Column(String(5),   nullable=False)
    location   = Column(String(120), nullable=True,  default="")
    priority   = Column(Enum(PriorityLevel), nullable=False,
                        default=PriorityLevel.medium)
