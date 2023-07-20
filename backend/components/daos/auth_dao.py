from typing import Optional

from components.db import get_engine
from components.models.auth.auth_user import AuthUser
from components.models.orm_models import AuthUserTbl
from components.utils.exceptions import UsernameExistsError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

_engine = get_engine()

def get_user_by_username(username: str) -> Optional[AuthUser]:
    """
    Gets an auth user based on a username

    :param username: username associated with the user
    :return AuthUser if exists, else None
    """
    try:
        with _engine.connect() as connection:
            stmt = select(AuthUserTbl).where(AuthUserTbl.username == username)
            result = connection.execute(stmt)
            user = result.first()
            return AuthUser(
                user_id=user.user_id,
                username=user.username,
                hashed_password=user.hashed_password,
            ) if user else None
    except Exception as e:
        raise Exception(f"An error occurred retrieving an auth user from the db: {e}")


def create_user(user_id: int, username: str, hashed_password: str) -> None:
    """
    Creates an auth user with the given information

    :except UsernameExistsError if the username already exists
    :except Exception if an error occurs communicating with the db
    """
    try:
        user = AuthUserTbl(
            user_id=user_id,
            username=username,
            hashed_password=hashed_password
        )
        with Session(_engine) as session:
            session.add(user)
            session.commit()
    except IntegrityError:
        raise UsernameExistsError(f"Cannot create user, username {username} already exists")
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")
