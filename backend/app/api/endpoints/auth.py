from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session
import httpx # For making requests during userinfo fetching for GitHub if needed

from app.core.auth import oauth
from app.core.config import settings
from app.core.security import create_access_token
from app.crud.crud_user import user as crud_user
from app.db.session import get_db
from app.schemas.user import UserCreateOAuth

router = APIRouter()

@router.get("/login/{provider}")
async def login_via_provider(provider: str, request: Request):
    if provider not in ["google", "github"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")

    # Construct the redirect_uri dynamically based on the provider
    # This should match exactly what's configured in the settings and the OAuth provider console
    redirect_uri = request.url_for(f'auth_callback', provider=provider)

    # For Authlib, redirect_uri might be taken from client registration if not passed here.
    # It's good to be explicit or ensure client registration has the correct one.
    # The redirect_uri in oauth.register (core/auth.py) for Google uses settings.GOOGLE_REDIRECT_URI
    # which is f"{settings.SERVER_HOST}/api/v1/auth/google/callback".
    # Let's ensure request.url_for generates this exact URI.
    # If SERVER_HOST is http://localhost:8000, then request.url_for('auth_callback', provider='google')
    # should produce 'http://localhost:8000/api/v1/auth/google/callback'

    # Correctly get the client (google or github)
    oauth_client = getattr(oauth, provider)
    if oauth_client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"OAuth client for {provider} not configured")

    return await oauth_client.authorize_redirect(request, redirect_uri)


@router.get("/auth/{provider}/callback", name="auth_callback")
async def auth_callback(provider: str, request: Request, db: Session = Depends(get_db)):
    if provider not in ["google", "github"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")

    oauth_client = getattr(oauth, provider)
    if oauth_client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"OAuth client for {provider} not configured")

    try:
        token_data = await oauth_client.authorize_access_token(request)
    except Exception as e:
        # Log the error e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not authorize access token: {str(e)}")

    user_info = None
    if provider == "google":
        user_info = await oauth_client.parse_id_token(request, token_data)
        # Or: user_info = token_data.get('userinfo') if server_metadata_url provides it directly
    elif provider == "github":
        # For GitHub, parse_id_token is not standard; usually, you fetch userinfo from the endpoint
        # Ensure the token_data contains 'access_token'
        access_token = token_data.get('access_token')
        if not access_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access token not found in GitHub response")

        # Fetch user info from GitHub API
        async with httpx.AsyncClient() as client:
            headers = {'Authorization': f'token {access_token}'}
            # The userinfo_endpoint is configured in oauth.register for github
            api_response = await client.get(oauth_client.userinfo_endpoint, headers=headers)
            if api_response.status_code != 200:
                raise HTTPException(status_code=api_response.status_code, detail="Could not fetch user info from GitHub")
            user_info_data = api_response.json()

            # Extract email, id, name from GitHub response
            # GitHub primary email might require a separate API call if not in main user info and scope `user:email` is used.
            # For simplicity, assume 'email' is available or can be None.
            # If 'email' is null, you might need to query /user/emails endpoint.
            user_info = {
                "email": user_info_data.get("email"),
                "sub": str(user_info_data.get("id")), # 'sub' is typically user ID for non-OpenID Connect providers
                "name": user_info_data.get("name") or user_info_data.get("login"),
                "picture": user_info_data.get("avatar_url"), # Example, can be stored if User model has picture field
                # GitHub specific fields
                "provider_user_id": str(user_info_data.get("id")),
            }
            # If primary email is null from main endpoint, try to get it from /user/emails
            if not user_info["email"]:
                emails_response = await client.get('https://api.github.com/user/emails', headers=headers)
                if emails_response.status_code == 200:
                    emails_data = emails_response.json()
                    primary_email = next((e['email'] for e in emails_data if e['primary']), None)
                    if primary_email:
                        user_info["email"] = primary_email

            if not user_info["email"]:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not available from GitHub. Please ensure your GitHub account has a public primary email.")


    if not user_info or not user_info.get("email"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not fetch user info or email from provider.")

    email = user_info.get("email")
    provider_user_id = str(user_info.get("sub") if provider == "google" else user_info.get("provider_user_id"))
    full_name = user_info.get("name")

    user_obj_in = UserCreateOAuth(email=email, full_name=full_name)

    try:
        db_user = crud_user.create_user_with_provider(
            db=db, obj_in=user_obj_in, provider=provider, provider_user_id=provider_user_id, full_name=full_name
        )
    except ValueError as e: # Catch custom ValueError from CRUD
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Log the error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error processing user data.")


    access_token = create_access_token(data={"sub": db_user.email})

    # Redirect to frontend, set cookie
    # FRONTEND_URL should be configured in settings
    response = RedirectResponse(url=settings.FRONTEND_URL + "/profile") # Or just FRONTEND_URL
    response.set_cookie(
        key=settings.JWT_COOKIE_NAME,
        value=f"{access_token}", # No "Bearer " prefix for cookies typically
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE, # Should be True in production (HTTPS)
        samesite=settings.JWT_COOKIE_SAMESITE,
        path="/", # Cookie available for all paths
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60 # Cookie expiry in seconds
    )
    return response

@router.post("/logout")
async def logout():
    response = Response(status_code=status.HTTP_200_OK, content={"message": "Successfully logged out"})
    response.delete_cookie(key=settings.JWT_COOKIE_NAME, path="/", samesite=settings.JWT_COOKIE_SAMESITE, secure=settings.JWT_COOKIE_SECURE)
    return response
