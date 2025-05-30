from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles # For potential admin static files

from app.api.endpoints import waitlist, auth, users, courses, lessons, sandbox # Import new routers
from app.admin import admin_router # Import the admin router
from app.core.config import settings

app = FastAPI(
    title="YuriODev Backend",
    version="0.1.0",
    # openapi_url=f"{settings.API_V1_STR}/openapi.json" # If you have API_V1_STR in settings
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
                      if isinstance(settings.BACKEND_CORS_ORIGINS, list)
                      else [settings.BACKEND_CORS_ORIGINS], # Handle string or list
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(waitlist.router, prefix="/api/v1", tags=["Waitlist"]) # Existing
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["Courses"])
app.include_router(lessons.router, prefix="/api/v1/lessons", tags=["Lessons"])
app.include_router(sandbox.router, prefix="/api/v1/sandbox", tags=["Sandbox"])

# Mount the admin router
app.include_router(admin_router.router) # Prefix is defined within admin_router.py

# Optional: Mount static files for admin if any custom CSS/JS for admin panel not inlined
# app.mount("/admin/static", StaticFiles(directory="app/admin/static"), name="admin_static")


@app.get("/")
async def root():
    return {"message": "Welcome to YuriODev Backend"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}
