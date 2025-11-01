# FastAPI application entry point with GraphQL integration and database setup
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from .schema import schema
from .database import Base, engine

Base.metadata.create_all(bind=engine)

graphql_app = GraphQLRouter(schema) # Endpoint router for GraphQL

app = FastAPI()  # Main FastAPI application instance
app.include_router(graphql_app, prefix="/task-api")