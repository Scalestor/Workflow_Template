from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from .base import Base

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String,nullable=False)
    rights = Column(String,nullable=False)
