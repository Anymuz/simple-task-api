# FastAPI application entry point with GraphQL integration and database setup
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

graphql_app = GraphQLRouter() # Endpoint router for GraphQL
app = FastAPI()  # Main FastAPI application instance
app.include_router(graphql_app, prefix="/task-api")