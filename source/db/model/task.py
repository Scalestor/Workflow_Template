from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    process_template_id = Column(Integer, ForeignKey('process_templates.id'), nullable=False)
    task_name = Column(String, nullable=False)
    task_description = Column(Text)
    assignee_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String, default='pending')
    
    process_template = relationship("ProcessTemplate", back_populates="tasks")
    assignee = relationship("User")
    history = relationship("TaskHistory", back_populates="task")