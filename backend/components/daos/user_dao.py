from typing import Optional

from components.models.user import User
from components.models.orm_models import UserTbl
from components.db import get_engine

from sqlalchemy import select

_engine = get_engine()

def get_user_by_id(id: int) -> Optional[User]:
    """
    Gets a user with a given id

    :param username: username associated with the user
    :return User if exists, else None
    """
    try:
        with _engine.connect() as connection:
            stmt = select(UserTbl).where(UserTbl.id == id)
            result = connection.execute(stmt)
            user = result.first()
            return User(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
            ) if user else None
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")
