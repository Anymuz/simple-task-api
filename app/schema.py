# Schema for GraphQL API using Strawberry - 
# This schema defines the GraphQL types and queries for the task management API.

# -------[ Imports ]--------
# Necessary imports for Strawberry, typing, and database session management
import strawberry
from typing import List, Optional
from strawberry.types import Info
from sqlalchemy.orm import Session
from graphql import GraphQLError

# Import Task model and database session local
from .models import Task
from .database import SessionLocal
#---------------------------

#-----[ Database Session ]-----
# Function to start, update then close a database session
def get_db():
    db = SessionLocal() # Start isolated session locally named db
    try: yield db # Use yield on db keeps ACID principles enforced
    finally: db.close() # Close session once fully complete
# End function
#------------------------------

# -------[ GraphQL Types ]--------
# Define TaskType for GraphQL schema
@strawberry.type
class TaskType:
    id: int
    title: str
    completed: bool
    created_at: Optional[str]
    updated_at: Optional[str]
# End type
#---------------------------------

#-------[ GraphQL Inputs ]--------
# Input for listing tasks with optional search filter
@strawberry.input
class TaskListInput:
    search: Optional[str] = None

# Input for operations on a task by ID
@strawberry.input
class TaskIdInput:
    id: int

# Input for creating tasks, takes title only
@strawberry.input
class NewTaskInput:
    title: str
# End input
#---------------------------------

#-------[ GraphQL Queries ]--------
@strawberry.type
class Query:
    # Retrieve all tasks with optional filters for search and completion status, defaults to none so tasks{} returns all tasks without need for args input = none.
    @strawberry.field
    def tasks(self, info: Info, input: Optional[TaskListInput] = None) -> List[TaskType]: # Return list of TaskType, use info for context to make scalable later
        db: Session = next(get_db()) # Get the next generated DB session
        query = db.query(Task) # Start query on Task model, acts like SELECT * FROM tasks

        # Filter by search argument if provided, filtering input type remains optional
        if input and input.search: 
            query = query.filter(Task.title.contains(input.search)) 
        # End if

        return query.all() # Return all matching tasks
    # End def

    # Retrieve a single task by its ID
    @strawberry.field
    def task(self, info: Info, input: TaskIdInput) -> Optional[TaskType]: # Optional used so null return when task not found.
        db: Session = next(get_db()) 
        task = db.query(Task).filter(Task.id == input.id).first() # Query for task by given ID, acts like SELECT * FROM tasks WHERE id = id
        return task
    # End def
# End queries
#---------------------------------

#-------[ GraphQL Mutations ]-------
@strawberry.type
class Mutation:
    # Create a new task using the provided input
    @strawberry.mutation
    def add_task(self, info: Info, input: NewTaskInput) -> TaskType: # Use input type to return TaskType
        db: Session = next(get_db()) 
        new_task = Task(title=input.title) # Define the new task from our input
        db.add(new_task)
        db.commit()
        db.refresh(new_task) # Refresh to get the generated ID and timestamps
        return new_task
    # End mutation

    # Toggle the completed status of a task by its ID
    @strawberry.mutation
    def toggle_task(self, info: Info, input: TaskIdInput) -> Optional[TaskType]:
        db: Session = next(get_db()) 
        task = db.query(Task).filter(Task.id == input.id).first()
        #  If task found, toggle its completed status
        if task:
            task.completed = not task.completed  # always set completed status to be opposite of current
            db.commit()
            db.refresh(task) # Refresh to updated timestamp
        return task
    # End mutation

    # Delete a task by its ID
    @strawberry.mutation
    def delete_task(self, info: Info, input: TaskIdInput) -> Optional[TaskType]:
        db: Session = next(get_db()) 
        task = db.query(Task).filter(Task.id == input.id).first()
        if task:
            db.delete(task) # Delete the task from the db session
            db.commit() # Commit the deletion to remove task permanently
            return task
        return None
# End class
#----------------------------------

schema = strawberry.Schema(query=Query, mutation=Mutation) # Create the schema with query and mutation

''''todo  next - Add bonus features:  
- update_task mutation 
- task_stats query?
- additional filters for tasks query  (completed status, date ranges?) '''