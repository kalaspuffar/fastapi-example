from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=True, default="new")
