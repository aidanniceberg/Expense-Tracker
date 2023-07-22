from datetime import datetime
from typing import List, Optional

from components.daos import expense_dao, expense_group_dao
from components.models.expense import Expense
from components.utils.exceptions import UnauthorizedError


def get_expenses_by_group(group_id: int, user_id: int, created_before: Optional[datetime] = None, created_after: Optional[datetime] = None) -> List[Expense]:
    """
    Gets expenses for a given group

    :param group_id: id of group to get expenses for
    :param user_id: id of user making the query
    :param created_before: only return expenses created before this date
    :param created_after: only return expenses created after this date
    :return list of expenses
    :except UnauthorizedError if the user does not belong to the requested group
    """
    if not expense_group_dao.user_is_member(user_id, group_id):
        raise UnauthorizedError("User does not belong to the requested group")
    return expense_dao.get_expenses_by_group(group_id=group_id, created_before=created_before, created_after=created_after)


def create_expense(author_id: int, title: str, price: float, group_id: int, description: Optional[str] = None) -> int:
    """
    Creates an expense

    :param author_id: id of user creating the expense
    :param title: title of the expense
    :param price: price of the expense
    :param group_id: id of group to tie the expense to
    :param description: expense description
    :return id of newly created expense
    :except Unauthorized error if the user does not belong to the requested group
    """
    if not expense_group_dao.user_is_member(author_id, group_id):
        raise UnauthorizedError("User does not belong to the requested group")
    return expense_dao.create_expense(author_id, title, price, group_id, description)


def update_expense(expense_id: int, user_id: int, title: Optional[str] = None, price: Optional[float] = None, description: Optional[str] = None):
    """
    Updates an expense

    :param expense_id: id of expense being updated
    :param user_id: id of user updating the expense
    :param title: updated title
    :param price: updated price
    :param description: updated description
    :return True if the expense was updated
    :except Unauthorized error if the user did not create the given expense
    """
    if not expense_dao.user_is_author(user_id, expense_id):
        raise UnauthorizedError("User did not create an expense with the provided id")
    return expense_dao.update_expense(id=expense_id, title=title, price=price, description=description)


def delete_expense(user_id: int, expense_id: int) -> bool:
    """
    Deletes an expense

    :param user_id: id of user deleting the expense
    :param expense_id: id of expense to delete
    :return True if the expense was deleted
    :except UnauthorizedError if the user did not create the given expense
    """
    if not expense_dao.user_is_author(user_id, expense_id):
        raise UnauthorizedError("User did not create an expense with the provided id")
    return expense_dao.delete_expense(expense_id)
