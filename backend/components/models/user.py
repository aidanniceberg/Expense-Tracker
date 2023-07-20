from pydantic import BaseModel

class User(BaseModel):
    """
    Represents a user
    """
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
