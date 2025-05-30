from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Load DATABASE_URL from environment variable
# Default to a local SQLite DB if not set (useful for local tests not in Docker)
# However, for this project, DATABASE_URL will be set by Docker Compose for the backend service.
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    # This case should ideally not happen when running within Docker via docker-compose.yml
    # as DATABASE_URL is provided there.
    # Fallback for scenarios where it might be run outside Docker without this env var.
    print("DATABASE_URL not set, using default SQLite path. THIS SHOULD NOT HAPPEN IN PRODUCTION/DOCKER.")
    SQLITE_DB_PATH = "sqlite:///./test.db" # Or some other local default
    DATABASE_URL = SQLITE_DB_PATH
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # SQLite specific
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency to get a DB session.
    Ensures the session is closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
