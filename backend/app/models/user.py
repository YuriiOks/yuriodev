from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Index
from sqlalchemy.dialects.postgresql import UUID # If using UUID for ID, otherwise Integer
import uuid # For UUID default

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # If using UUIDs for id:
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True) # Nullable if using OAuth-only login initially

    full_name = Column(String, index=True, nullable=True)

    # OAuth provider details
    provider = Column(String, nullable=True) # e.g., "google", "github"
    provider_user_id = Column(String, nullable=True) # User ID from the OAuth provider

    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("ix_users_provider_provider_user_id", "provider", "provider_user_id", unique=True),
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', provider='{self.provider}')>"
