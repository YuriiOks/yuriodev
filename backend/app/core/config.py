from pydantic_settings import BaseSettings # Using pydantic-settings
from typing import List, Union
import os

class Settings(BaseSettings):
    APP_ENV: str = "development"
    SERVER_HOST: str = "http://localhost:8000" # Used for redirect URIs, ensure it matches your setup

    # Database
    DATABASE_URL: str = "postgresql://yuriodev:yuriodevpass@postgres:5432/yuriodevdb" # Default, overridden by env

    # JWT settings
    SECRET_KEY: str = "supersecretkeythatshouldbechanged" # CHANGE THIS IN PRODUCTION
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # 30 minutes
    # For cookies
    JWT_COOKIE_NAME: str = "yuriodev_access_token"
    JWT_COOKIE_SECURE: bool = False # Set to True in production (HTTPS)
    JWT_COOKIE_SAMESITE: str = "lax" # "lax" or "strict" or "none" (if "none", must be Secure)

    # CORS settings
    # Backend server URL, if different from SERVER_HOST (e.g., if API is on a different port/domain than OAuth redirects)
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = ["http://localhost:3000", "http://localhost"] # Frontend URL
                                                                                              # Add other origins as needed

    # OAuth Providers - Client ID and Secret should be loaded from environment variables
    # Google
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "your_google_client_id_placeholder")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "your_google_client_secret_placeholder")
    # Redirect URI must match exactly what's configured in Google Cloud Console
    GOOGLE_REDIRECT_URI: str = f"{SERVER_HOST}/api/v1/auth/google/callback"

    # GitHub
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "your_github_client_id_placeholder")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "your_github_client_secret_placeholder")
    # Redirect URI must match exactly what's configured in GitHub OAuth App settings
    GITHUB_REDIRECT_URI: str = f"{SERVER_HOST}/api/v1/auth/github/callback"

    # Frontend URL for redirects
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")


    # For pydantic-settings, to load from .env file if present (optional)
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Pydantic V2 way for case_sensitive:
        # case_sensitive = True
        # For Pydantic V1 (if BaseSettings is from old pydantic):
        # case_sensitive = True # Ensure env var names match exactly


settings = Settings()

# Verify critical OAuth settings (optional, but good for early warning)
# if settings.APP_ENV != "development": # Only check in non-dev environments if placeholders are used
#     if "placeholder" in settings.GOOGLE_CLIENT_ID or "placeholder" in settings.GOOGLE_CLIENT_SECRET:
#         print("WARNING: Google OAuth credentials are using placeholder values.")
#     if "placeholder" in settings.GITHUB_CLIENT_ID or "placeholder" in settings.GITHUB_CLIENT_SECRET:
#         print("WARNING: GitHub OAuth credentials are using placeholder values.")
