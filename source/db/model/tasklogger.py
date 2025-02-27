from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class TaskHistory(Base):
    __tablename__ = 'task_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(datetime.timezone.utcnow()))
    
    task = relationship("Task", back_populates="history")