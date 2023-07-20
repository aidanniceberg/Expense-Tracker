from typing import Optional

from components.models.auth.auth_user import AuthUser
from components.models.orm_models import AuthUserTbl
from components.db import get_engine

from sqlalchemy import select

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
