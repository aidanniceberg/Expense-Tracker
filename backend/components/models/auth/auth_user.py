from pydantic import BaseModel

class AuthUser(BaseModel):
    """
    Represents a user for authentication purposes
    """
    user_id: int
    username: str
    hashed_password: str
