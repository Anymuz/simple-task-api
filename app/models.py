# Datatype imports, now timestamp function and column definition function.
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func 

from .database import Base # Base from database.py to extend for our model.

# Class for a task object in DB - extends Base and maps to the tasks table in the database
class Task(Base):
    __tablename__ = "tasks" 

    id = Column(Integer, primary_key=True, index=True) # Primary key column - auto-incremented
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), # Timestamp when created on commit
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), # Timestamp when last updated at first will be creation time
        onupdate=func.now(), # Update timestamp on each update
        nullable=False
    )
# End of Task model class