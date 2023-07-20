from typing import Annotated
from components.models.user import User
from components.models.auth.token import Token
from components.services import auth_service


from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

AUTH_TAG = "Authentication"

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/token", tags=[AUTH_TAG])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    return auth_service.login(form_data)

@app.get("/users/me", tags=[AUTH_TAG])
def me(current_user: Annotated[User, Depends(auth_service.get_current_user)]) -> User:
    return current_user
