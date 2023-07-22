from datetime import datetime
from typing import Annotated, List, Optional

from components.models.auth.token import Token
from components.models.expense import Expense
from components.models.expense_group import ExpenseGroup
from components.models.user import User
from components.services import (
    auth_service,
    expense_group_service,
    expense_service,
    user_service
)
from components.utils.exceptions import (
    DoesNotExistError,
    UnauthorizedError,
    UsernameExistsError
)
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm

AUTH_TAG = "Authentication"
USERS_TAG = "Users"
GROUPS_TAG = "Groups"
EXPENSES_TAG = "Expenses"

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/users", tags=[USERS_TAG])
def create_user(username: str, password: str, first_name: str, last_name: str, email: str) -> bool:
    try:
        hashed_password = auth_service.hash_password(password)
        user_service.create_user(username, hashed_password, first_name, last_name, email)
        return True
    except UsernameExistsError:
        raise HTTPException(status_code=403, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/groups", tags=[GROUPS_TAG])
def get_groups(user: Annotated[User, Depends(auth_service.get_current_user)]) -> List[ExpenseGroup]:
    try:
        return expense_group_service.get_groups(user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/groups/{id}/members", tags=[GROUPS_TAG])
def get_group_members(id: int, user: Annotated[User, Depends(auth_service.get_current_user)]) -> List[User]:
    try:
        return expense_group_service.get_group_members(user.id, id)
    except UnauthorizedError as ue:
        raise HTTPException(status_code=401, detail=str(ue))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/groups", tags=[GROUPS_TAG])
def create_group(author: Annotated[User, Depends(auth_service.get_current_user)], name: str, members: Annotated[List[int], Query()] = []) -> int:
    try:
        return expense_group_service.create_group(author.id, name, members)
    except DoesNotExistError:
        raise HTTPException(status_code=404, detail="Group member not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/groups/{id}/expenses", tags=[GROUPS_TAG])
def get_expenses(user: Annotated[User, Depends(auth_service.get_current_user)], id: int, created_before: Optional[datetime] = None, created_after: Optional[datetime] = None) -> List[Expense]:
    try:
        return expense_service.get_expenses_by_group(group_id=id, user_id=user.id, created_before=created_before, created_after=created_after)
    except UnauthorizedError as ue:
        raise HTTPException(status_code=401, detail=str(ue))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/groups/{id}/expenses", tags=[GROUPS_TAG])
def create_expense(author: Annotated[User, Depends(auth_service.get_current_user)], title: str, price: float, id: int, description: Optional[str] = None) -> int:
    try:
        return expense_service.create_expense(author.id, title, price, id, description)
    except DoesNotExistError as dne:
        raise HTTPException(status_code=404, detail=str(dne))
    except UnauthorizedError as ue:
        raise HTTPException(status_code=401, detail=str(ue))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/expenses/{id}", tags=[EXPENSES_TAG])
def update_expense(user: Annotated[User, Depends(auth_service.get_current_user)], id: int, title: Optional[str] = None, price: Optional[float] = None, description: Optional[str] = None) -> bool:
    try:
        return expense_service.update_expense(expense_id=id, user_id=user.id, title=title, price=price, description=description)
    except UnauthorizedError as ue:
        raise HTTPException(status_code=401, detail=str(ue))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/expenses/{id}", tags=[EXPENSES_TAG])
def delete_expense(user: Annotated[User, Depends(auth_service.get_current_user)], id: int) -> bool:
    try:
        return expense_service.delete_expense(user.id, id)
    except DoesNotExistError as dne:
        raise HTTPException(status_code=404, detail=str(dne))
    except UnauthorizedError as ue:
        raise HTTPException(status_code=401, detail=str(ue))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/token", tags=[AUTH_TAG])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    try:
       return auth_service.login(form_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/me", tags=[AUTH_TAG])
def me(current_user: Annotated[User, Depends(auth_service.get_current_user)]) -> User:
    return current_user
