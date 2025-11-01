# Schema for GraphQL API using Strawberry - 
# This schema defines the GraphQL types and queries for the task management API.

# -------[ Imports ]--------
# Necessary imports for Strawberry, typing, and database session management
import strawberry
from typing import List, Optional
from strawberry.types import Info
from sqlalchemy.orm import Session

# Import Task model and database session local
from .models import Task
from .database import SessionLocal

# Function to start, update then close a database session
def get_db():
    db = SessionLocal() # Start isolated session locally named db
    try: yield db # Use yield on db keeps ACID principles enforced
    finally: db.close() # Close session once fully complete
# End function
#--------------------------------

# -------[ GraphQL Types ]--------
# Define TaskType for GraphQL schema
@strawberry.type
class TaskType:
    id: int
    title: str
    completed: bool
    created_at: Optional[str]
    updated_at: Optional[str]
# End class
#--------------------------------

#-------[ GraphQL Inputs ]--------
# Define input for creating tasks, takes title only
@strawberry.input
class TaskInput:
    title: str
# End class
#---------------------------------

#-------[ GraphQL Queries ]--------
@strawberry.type
class Query:
    # Retrieve all tasks with optional filters for search and completion status
    @strawberry.field
    def tasks(self, info: Info, search: Optional[str] = None) -> List[TaskType]:
        db: Session = next(get_db())# Get the next generated DB session
        query = db.query(Task) # Start query on Task model
        if search: query = query.filter(Task.title.contains(search)) # Filter if provided
        return query.all() # Return all matching tasks
    # End field
# End class queries
#--------------------------------

#-------[ GraphQL Mutations ]-------
@strawberry.type
class Mutation:
    # Create a new task using the provided input
    @strawberry.mutation
    def add_task(self, info: Info, input: TaskInput) -> TaskType: # Use input type to return TaskType
        db: Session = next(get_db()) 
        new_task = Task(title=input.title) # Define the new task from our input
        db.add(new_task)
        db.commit()
        db.refresh(new_task) # Refresh to get the generated ID and timestamps
        return new_task
    # End def
# End class
#--------------------------------

schema = strawberry.Schema(query=Query, mutation=Mutation) # Create the schema with query and mutation
# todo  next - complete schema.py with toggle and delete mutations, and task by id query