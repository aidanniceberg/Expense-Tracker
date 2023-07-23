from typing import List

from components.daos import expense_group_dao, user_dao
from components.models.expense_group import ExpenseGroup
from components.models.user import User
from components.utils.exceptions import DoesNotExistError, ExistsError, UnauthorizedError


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
    if not expense_group_dao.user_is_member(user_id, group_id):
        raise UnauthorizedError("User does not belong to the requested group")
    return user_dao.get_group_members(group_id)


def add_group_member(member_id: int, group_id: int, user_id: int) -> bool:
    """
    Adds a member to a group

    :param member_id: id of member adding the user
    :param group_id: id of group the member is being added to
    :param user_id: id of user being added to the group
    :except Unauthorized error if the user does not belong to the requested group
    :except ExistsError if the user being added is already a member of the group
    """
    if not user_dao.user_exists(user_id):
        raise DoesNotExistError("Requested user does not exist")
    elif not expense_group_dao.user_is_member(member_id, group_id):
        raise UnauthorizedError("User making request does not belong to the requested group")
    elif expense_group_dao.user_is_member(user_id, group_id):
        raise ExistsError("User requested to be added to the group is already a member")
    return expense_group_dao.add_member(group_id, user_id)


def create_group(author_id: int, name: str, members: List[int] = []) -> int:
    """
    Creates an expense group

    :param author_id: id of user creating the group
    :param name: name of the group
    :param members: ids of users in the group
    :return id of newly created group
    """
    return expense_group_dao.create_group(author_id, name, members)
