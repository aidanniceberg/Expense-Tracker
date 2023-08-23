from datetime import datetime, timedelta
from typing import Annotated, Optional

from components.constants import ACCESS_TOKEN_KEY
from components.daos import auth_dao, user_dao
from components.models.auth.auth_user import AuthUser
from components.models.auth.token import Token
from components.models.user import User
from components.utils.exceptions import CredentialsError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    Authenticates and logs in a user

    :param form_data: data containing username and password
    :return access token
    """
    user = authenticate(form_data.username, form_data.password)
    if not user:
        raise CredentialsError("Could not validate credentials")
    access_token = create_access_token(user.username)
    return Token(
        access_token=access_token,
        token_type="bearer"
    )


def authenticate(username: str, password: str) -> Optional[AuthUser]:
    """
    Authenticates a user

    :param username: inputted username
    :param password: inputted password
    :return auth user if properly authenticated
    """
    user = _get_auth_user_by_username(username)
    return (
        user
        if user and _pwd_context.verify(password, user.hashed_password)
        else None
    )


def hash_password(password: str) -> str:
    """
    Hashes a plaintext password

    :param password: plaintext password to hash
    :return hashed password
    """
    return _pwd_context.hash(password)


def get_current_user(token: Annotated[str, Depends(_oauth2_scheme)]) -> User:
    """
    Given a token, gets the currently authenticated user

    :param token: access token
    :return current user
    :except 401 exception if user is not properly authenticated
    :except 500 exception if the user is properly authenticated but not found in the db
    """
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise CredentialsError("Could not validate credentials")
    
    username = payload.get("sub")
    if username is None:
        raise CredentialsError("Could not validate credentials")
    
    exp_timestamp = payload.get("exp")
    if exp_timestamp is None or datetime.fromtimestamp(exp_timestamp) < datetime.now():
        raise CredentialsError("Acess token is expired")

    auth_user = _get_auth_user_by_username(username)
    if auth_user is None:
        raise CredentialsError("Could not validate credentials")
    
    user = _get_user_by_id(auth_user.user_id)
    if user is None:
        raise Exception("User properly authenticated but not found in db")
    
    return user


def create_access_token(username: str, ttl: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """
    Creates an access token for a given user

    :param username: username of the user the token is being generated for
    :param ttl: access token expiration time
    :return access token
    """
    token = {
        "exp": datetime.utcnow() + ttl,
        "sub": username,
    }
    return jwt.encode(token, ACCESS_TOKEN_KEY, algorithm=ALGORITHM)


def _get_auth_user_by_username(username: str) -> Optional[AuthUser]:
    """
    Gets an auth user based on a username

    :param username: username associated with the user
    :return AuthUser if exists, else None
    """
    return auth_dao.get_user_by_username(username)


def _get_user_by_id(id: int) -> Optional[User]:
    """
    Gets a user with a given id

    :param username: username associated with the user
    :return User if exists, else None
    """
    return user_dao.get_user_by_id(id)
