# Database configuration and session management
# Import necessary modules from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Constant to define using SQLite database file stored in project directory
DATABASE_URL = "sqlite:///./taskData.db"

# Create the SQLAlchemy engine and session maker usinng SQLite as defined in DATABASE_URL:
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) 
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) 
Base = declarative_base() # Base class for our models to extend