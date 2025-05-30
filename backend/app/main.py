from fastapi import FastAPI
from app.api.endpoints import waitlist # Import the new router

app = FastAPI(title="YuriODev Backend", version="0.1.0")

# Include the waitlist router
app.include_router(waitlist.router, prefix="/api/v1", tags=["Waitlist"])

@app.get("/")
async def root():
    return {"message": "Welcome to YuriODev Backend"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}

