from datetime import datetime
from pydantic import BaseModel

from components.models.user import User

class ExpenseGroup(BaseModel):
    """
    Represents an expense group
    """
    id: int
    name: str
    author: User
    created_date: datetime
