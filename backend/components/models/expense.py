from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Expense(BaseModel):
    """
    Represents an expense
    """
    id: int
    title: str
    description: Optional[str]
    price: float
    date: datetime
    author_id: int
