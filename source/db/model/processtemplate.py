from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class ProcessTemplate(Base):
    __tablename__ = 'process_templates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    tasks = relationship("Task", back_populates="process_template")