from app.database import db
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

def get_db():
    try:
        yield db
    finally:
        db.close()

# 
@app.get("/api/healthchecker")
def root(db=Depends(get_db)):
    return {"message": "Welcome to FastAPI with MongoDB"}
