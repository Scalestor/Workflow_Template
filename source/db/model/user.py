from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from .base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String,nullable=False)





