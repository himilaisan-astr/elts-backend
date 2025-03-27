from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
from app.database import engine, Base, get_db
from app.models import User
from app.routes import auth, api

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ELTS School API",
    description="API for ELT School of English Admin Dashboard",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:3000",
    "http://localhost:8000",  # Backend for development
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(
    auth.router,
    prefix="/api",
    tags=["Authentication"]
)

app.include_router(
    api.router,
    prefix="/api",
)

@app.get("/api/health", tags=["Dashboard"])
def health_check():
    return {"status": "healthy", "service": "ELTS Backend"}

@app.get("/", tags=["Dashboard"])
async def root():
    return {
        "message": "Welcome to ELTS School API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)