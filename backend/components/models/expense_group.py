from pydantic import BaseModel

class ExpenseGroup(BaseModel):
    """
    Represents an expense group
    """
    id: int
    name: str
    author_id: int
