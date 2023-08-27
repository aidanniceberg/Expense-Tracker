from datetime import datetime
from typing import List

from components.db import get_engine
from components.models.expense_group import ExpenseGroup
from components.models.orm_models import (ExpenseGroupMembersTbl,
                                          ExpenseGroupTbl, UserTbl)
from components.models.user import User
from components.utils.exceptions import DoesNotExistError
from sqlalchemy import and_, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

_engine = get_engine()

def get_groups(user_id: int) -> List[ExpenseGroup]:
    """
    Gets all expense groups for a given user

    :param user_id: id of user to get the groups for
    :except Exception if an error occurs communicating with the db
    """
    try:
        with Session(_engine) as session:
            groups = (
                session
                .query(ExpenseGroupTbl)
                .join(ExpenseGroupMembersTbl)
                .filter(ExpenseGroupMembersTbl.c.user_id == user_id)
            )
            return [
                ExpenseGroup(
                    id=group.id,
                    name=group.name,
                    created_date=group.created_date,
                    author=User(
                        id=group.author.id,
                        username=group.author.username,
                        first_name=group.author.first_name,
                        last_name=group.author.last_name,
                        email=group.author.email,
                    )
                )
                for group in groups
            ]
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")


def create_group(author_id: int, name: str, members: List[int] = []) -> int:
    """
    Creates an expense group

    :param author_id: id of user creating the group
    :param name: name of the group
    :param members: ids of users in the group
    :return group id
    :except DoesNotExistError if the a user reference does not exist
    :except Exception if an error occurs communicating with the db
    """
    try:
        with Session(_engine) as session:
            group = ExpenseGroupTbl(
                name=name,
                author_id=author_id,
                created_date=datetime.utcnow(),
            )
            session.add(group)
            session.flush()
            session.refresh(group)
            for id in [author_id, *members]:
                stmt = insert(ExpenseGroupMembersTbl).values(
                    group_id=group.id,
                    user_id=id,
                )
                session.execute(stmt)
            session.commit()
            return group.id
    except IntegrityError:
        raise DoesNotExistError(f"One or more expense group members do not exist")
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")


def add_member(group_id: int, user_id: int) -> bool:
    """
    Adds a member to a group

    :param group_id: id of group the member is being added to
    :param user_id: id of user being added to the group
    :except Exception if an error occurs communicating with the db
    """
    try:
        with Session(_engine) as session:
            stmt = insert(ExpenseGroupMembersTbl).values(
                group_id=group_id,
                user_id=user_id,
            )
            session.execute(stmt)
            session.commit()
            return True
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")


def user_is_member(user_id: int, group_id: int) -> bool:
    """
    Determines if a user is a member of a given group

    :param user_id: id of user
    :param group_id: id of group
    :return true if the user is a member of the group
    """
    try:
        with Session(_engine) as session:
            stmt = select(ExpenseGroupMembersTbl).where(
                and_(
                    ExpenseGroupMembersTbl.c.user_id == user_id,
                    ExpenseGroupMembersTbl.c.group_id == group_id
                )
            )
            return session.execute(stmt).rowcount > 0
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")
