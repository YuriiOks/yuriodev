from authlib.integrations.starlette_client import OAuth
from app.core.config import settings

oauth = OAuth()

# Google OAuth Client
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'redirect_url': settings.GOOGLE_REDIRECT_URI # Ensure this is explicitly set if not auto-detected
    }
)

# GitHub OAuth Client
oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    userinfo_endpoint='https://api.github.com/user', # Standard endpoint to get user info
    userinfo_compliance_fix=None, # No specific fix needed usually
    client_kwargs={'scope': 'user:email read:user'}, # read:user for public profile, user:email for primary email
)
