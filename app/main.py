from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1 import users, notes
from app.core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run before the app starts
    print("🚀 Starting up ProNotes+...")
    await create_db_and_tables()
    print("✅ Database tables ready.")
    yield
    # Shutdown: Run when app stops (optional)
    print("🛑 Shutting down ProNotes+...")

# Initialize FastAPI with lifespan
app = FastAPI(
    title="ProNotes+",
    version="1.0.0",
    lifespan=lifespan  # ← Modern way to handle startup/shutdown
)

# Include routers
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(notes.router, prefix="/api/v1", tags=["notes"])


@app.get("/")
def root():
    return {"status": "🔥 ProNotes+ LIVE"}