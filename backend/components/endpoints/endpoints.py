from typing import Annotated, List

from components.models.auth.token import Token
from components.models.user import User
from components.models.expense_group import ExpenseGroup
from components.services import auth_service, expense_group_service, user_service
from components.utils.exceptions import UsernameExistsError, DoesNotExistError
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm

AUTH_TAG = "Authentication"
USERS_TAG = "Users"
GROUPS_TAG = "Groups"

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
def get_groups(id: int, user: Annotated[User, Depends(auth_service.get_current_user)]) -> List[User]:
    try:
        return expense_group_service.get_group_members(user.id, id)
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


@app.post("/token", tags=[AUTH_TAG])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    try:
       return auth_service.login(form_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/me", tags=[AUTH_TAG])
def me(current_user: Annotated[User, Depends(auth_service.get_current_user)]) -> User:
    return current_user
