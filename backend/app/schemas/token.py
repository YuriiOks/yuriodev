from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # This will store the subject ('sub') of the token, which is the user's email or ID
    # It can be extended with other data if needed (e.g. scopes)
    sub: Optional[str] = None # 'sub' is standard JWT claim for subject
    # Pydantic v1 used 'id' or 'username' often, but 'sub' is more standard for JWT
    # For this project, 'sub' will store the user's email.
    # email: Optional[str] = None # Alternative if you prefer explicit field name
