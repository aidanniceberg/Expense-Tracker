from typing import Annotated

from components.models.auth.token import Token
from components.models.user import User
from components.services import auth_service, user_service
from components.utils.exceptions import UsernameExistsError
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

AUTH_TAG = "Authentication"
USERS_TAG = "Users"

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/users/create", tags=[USERS_TAG])
def create_user(username: str, password: str, first_name: str, last_name: str, email: str) -> bool:
    try:
        hashed_password = auth_service.hash_password(password)
        user_service.create_user(username, hashed_password, first_name, last_name, email)
        return True
    except UsernameExistsError:
        raise HTTPException(status_code=403, detail="Username already exists")
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
