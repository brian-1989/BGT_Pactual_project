from app.endpoints import subscription, cancellation
from app.start_db import initialize_collections
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Initialize the application
app = FastAPI()

# Set up the Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data in the DB
initialize_collections()

# Include the router for related routes
app.include_router(subscription.router, prefix="/api/v1")
app.include_router(cancellation.router, prefix="/api/v1")

# 
@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}
