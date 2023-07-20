from pydantic import BaseModel

class Token(BaseModel):
    """
    Represents an access token
    """
    access_token: str
    token_type: str
