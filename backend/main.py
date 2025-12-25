from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
import traceback
from lib.note_management_lib import *
from sqlmodel import create_engine, Session
from sqlmodel import text
from contextlib import asynccontextmanager
from loguru import logger


DATABASE_URL = "sqlite:///notes.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session





@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    with next(get_session()) as session:
        result = session.exec(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='notes'")
        ).first()
        if not result:
            raise RuntimeError("notes table does not exist!")
        else:
            logger.info("notes table exists!")

    # Yield control to the app
    yield
    # Shutdown code (optional)

# Get base path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_PATH = os.path.join(BASE_DIR, "frontend")

print(f"BASE_DIR: {BASE_DIR}")
print(f"FRONTEND_PATH: {FRONTEND_PATH}")

# Create FastAPI app
app = FastAPI(title="Notes API", lifespan=lifespan)
        

# API Routes MUST be defined before mounting static files
@app.get("/api/hello")
async def hello():
    """Simple API endpoint"""
    return {"message": "Hello from FastAPI!"}

@app.post("/api/data")
async def receive_data(data: dict):
    """Receive data from frontend"""
    return {"received": data}



















# Serve React build files (Vite outputs to 'dist' folder)
dist_path = os.path.join(FRONTEND_PATH, "dist")
print(f"Checking dist path: {dist_path}")
print(f"Dist exists: {os.path.exists(dist_path)}")
print(f"Is dir: {os.path.isdir(dist_path)}")

if os.path.exists(dist_path) and os.path.isdir(dist_path):
    print(f"Using dist path: {dist_path}")
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")
else:
    # During development, serve from public directory
    public_path = os.path.join(FRONTEND_PATH, "public")
    print(f"Using public path: {public_path}")
    app.mount("/", StaticFiles(directory=public_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
