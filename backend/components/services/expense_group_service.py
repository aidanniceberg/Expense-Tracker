from typing import List

from components.daos import expense_group_dao, user_dao
from components.models.expense_group import ExpenseGroup
from components.models.user import User
from components.utils.exceptions import UnauthorizedError


def get_groups(user_id: int) -> List[ExpenseGroup]:
    """
    Gets all expense groups for a given user

    :param user_id: id of user to get the groups for
    :return list of expense groups
    """
    return expense_group_dao.get_groups(user_id)


def get_group_members(user_id: int, group_id: int) -> List[User]:
    """
    Gets all members for a given group. If the user tries to query a group they don't belong to, throw an error

    :param user_id: id of user making the query
    :param group_id: id of group to get members for
    :return list of users who are members of the group
    """
    if not _is_member(user_id, group_id):
        raise UnauthorizedError("User does not belong to the requested group")
    return user_dao.get_group_members(group_id)


def create_group(author_id: int, name: str, members: List[int] = []) -> int:
    """
    Creates an expense group

    :param author_id: id of user creating the group
    :param name: name of the group
    :param members: ids of users in the group
    :return id of newly created group
    """
    return expense_group_dao.create_group(author_id, name, members)


def _is_member(user_id: int, group_id: int) -> bool:
    """
    Determines if a user is a member of a given group

    :param user_id: id of user
    :param group_id: id of group
    :return true if the user is a member of the group
    """
    return expense_group_dao.user_is_member(user_id, group_id)
