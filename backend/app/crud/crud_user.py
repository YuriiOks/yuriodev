from typing import Optional, Any
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreateOAuth # Will define this schema later
from app.core.security import get_password_hash # For traditional user creation, if added

class CRUDUser:
    def get_user(self, db: Session, user_id: Any) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_user_by_provider_details(
        self, db: Session, *, provider: str, provider_user_id: str
    ) -> Optional[User]:
        return (
            db.query(User)
            .filter(User.provider == provider, User.provider_user_id == provider_user_id)
            .first()
        )

    def create_user_with_provider(
        self, db: Session, *, obj_in: UserCreateOAuth, provider: str, provider_user_id: str, full_name: Optional[str] = None
    ) -> User:
        """
        Create a new user via OAuth provider or retrieve if already exists.
        obj_in contains email.
        """
        db_user = self.get_user_by_provider_details(db, provider=provider, provider_user_id=provider_user_id)
        if db_user:
            # Optionally update user details like full_name if they changed
            if full_name and db_user.full_name != full_name:
                db_user.full_name = full_name
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
            return db_user

        # Check if a user with this email already exists (e.g., signed up with another provider or email/pass)
        existing_email_user = self.get_user_by_email(db, email=obj_in.email)
        if existing_email_user:
            # This case needs careful handling.
            # Option 1: Link provider to existing account if authenticated and user confirms. (Complex)
            # Option 2: Forbid and ask user to log in with the original method. (Simpler for MVP)
            # Option 3: If original account has no provider details, link this one.
            if not existing_email_user.provider: # If existing user has no provider, link it.
                existing_email_user.provider = provider
                existing_email_user.provider_user_id = provider_user_id
                if full_name and not existing_email_user.full_name:
                     existing_email_user.full_name = full_name
                db.add(existing_email_user)
                db.commit()
                db.refresh(existing_email_user)
                return existing_email_user
            else:
                # User with this email exists and is already linked to a provider (or email/pass).
                # Raise an error or handle as per product decision.
                # For now, let's prevent creation if email is tied to another provider account.
                # This logic might need refinement based on UX choices for account linking.
                if existing_email_user.provider != provider:
                    raise ValueError(
                        f"User with email {obj_in.email} already exists with a different login method."
                    )
                # If it's the same provider, something is wrong (should have been caught by get_user_by_provider_details)
                # This path should ideally not be reached if provider check is first.

        # Create new user
        db_user = User(
            email=obj_in.email,
            full_name=full_name,
            provider=provider,
            provider_user_id=provider_user_id,
            is_active=True, # OAuth users are active by default
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    # Example for traditional username/password, not used for OAuth initial creation
    # def create_user_with_password(self, db: Session, *, obj_in: UserCreateTraditional) -> User:
    #     db_user = User(
    #         email=obj_in.email,
    #         hashed_password=get_password_hash(obj_in.password),
    #         full_name=obj_in.full_name,
    #         is_active=True, # Or False if email verification is needed
    #     )
    #     db.add(db_user)
    #     db.commit()
    #     db.refresh(db_user)
    #     return db_user

user = CRUDUser()
