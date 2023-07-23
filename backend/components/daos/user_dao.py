from typing import List, Optional

from components.db import get_engine
from components.models.orm_models import ExpenseGroupMembersTbl, UserTbl
from components.models.user import User
from components.utils.exceptions import UsernameExistsError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

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


def get_group_members(group_id: int) -> List[User]:
    """
    Gets all members for a given group. If the user tries to query a group they don't belong to, throw an error

    :param group_id: id of group to get members for
    :return list of users who are members of the group
    :except Exception if an error occurs communicating with the db
    """
    try:
        with Session(_engine) as session:
            users = (
                session
                .query(UserTbl)
                .join(ExpenseGroupMembersTbl)
                .filter(ExpenseGroupMembersTbl.c.group_id == group_id)
            )
            return [
                User(
                    id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email
                )
                for user in users
            ]
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")


def create_user(username: str, first_name: str, last_name: str, email: str) -> int:
    """
    Creates a user with the given information

    :return id of created user
    :except UsernameExistsError if the username already exists
    :except Exception if an error occurs communicating with the db
    """
    try:
        with Session(_engine) as session:
            user = UserTbl(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            session.add(user)
            session.flush()
            session.refresh(user)
            session.commit()
            return user.id
    except IntegrityError:
        raise UsernameExistsError(f"Cannot create user, username {username} already exists")
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")


def user_exists(user_id: int) -> bool:
    """
    Determines if a user exists

    :param user_id: user being checked
    :return True if the user exist
    :except Exception if an error occurs communicating with the db
    """
    try:
        with Session(_engine) as session:
            stmt = select(UserTbl).where(UserTbl.id == user_id)
            result = session.scalars(stmt).all()
            return len(result) > 0
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")
