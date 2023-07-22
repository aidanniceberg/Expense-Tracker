from datetime import datetime
from typing import List, Optional

from components.db import get_engine
from components.models.expense import Expense
from components.models.orm_models import ExpenseTbl
from components.utils.exceptions import DoesNotExistError
from sqlalchemy import and_, delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

_engine = get_engine()


def get_expenses_by_group(group_id: int, created_before: Optional[datetime] = None, created_after: Optional[datetime] = None) -> List[Expense]:
    """
    Gets expenses for a given group

    :param group_id: id of group to get expenses for
    :param created_before: only return expenses created before this date
    :param created_after: only return expenses created after this date
    :return list of expenses
    :except Exception if an error occurs communicating with the db
    """
    try:
        with Session(_engine) as session:
            stmt = select(ExpenseTbl).where(ExpenseTbl.group_id == group_id)
            if created_before is not None:
                stmt = stmt.where(ExpenseTbl.date < created_before)
            if created_after is not None:
                stmt = stmt.where(ExpenseTbl.date > created_after)
            stmt_ordered = stmt.order_by(ExpenseTbl.date)
            expenses = session.scalars(stmt_ordered).all()
            return [
                Expense(
                    id=expense.id,
                    title=expense.title,
                    description=expense.description,
                    price=expense.price,
                    date=expense.date,
                    author_id=expense.author_id,
                )
                for expense in expenses
            ]
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")


def create_expense(author_id: int, title: str, price: float, group_id: int, description: Optional[str] = None) -> int:
    """
    Creates an expense

    :param author_id: id of user creating the expense
    :param title: title of the expense
    :param price: price of the expense
    :param group_id: id of group to tie the expense to
    :param description: expense description
    :return id of newly created expense
    :except DoesNotExistError if the user reference does not exist
    :except Exception if an error occurs communicating with the db
    """
    try:
        with Session(_engine) as session:
            expense = ExpenseTbl(
                title=title,
                description=description,
                price=price,
                date=datetime.utcnow(),
                author_id=author_id,
                group_id=group_id,
            )
            session.add(expense)
            session.flush()
            session.refresh(expense)
            session.commit()
            return expense.id
    except IntegrityError:
        raise DoesNotExistError("Author or group does not exist")
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")


def update_expense(id: int, title: Optional[str] = None, price: Optional[float] = None, description: Optional[str] = None) -> bool:
    """
    Updates an expense

    :param id: id of expense being updated
    :param title: updated title
    :param price: updated price
    :param description: updated description
    :return True if the expense was updated
    :except Exception if an error occurs communicating with the db
    """
    update_values = {}
    if title is not None:
        update_values["title"] = title
    if price is not None:
        update_values["price"] = price
    if description is not None:
        update_values["description"] = description
    try:
        with Session(_engine) as session:
            stmt = update(ExpenseTbl).where(ExpenseTbl.id == id).values(update_values)
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")


def delete_expense(id: int) -> bool:
    """
    Deletes an expense

    :param id: id of expense to delete
    :return True if expense was deleted
    :except Exception if an error occurs communicating with the db
    """
    try:
        with Session(_engine) as session:
            stmt = delete(ExpenseTbl).where(ExpenseTbl.id == id)
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")


def user_is_author(user_id: int, expense_id: int) -> bool:
    """
    Determines if a given user is the author of an expense

    :param user_id: user
    :param expense_id: expense
    :return true if the user created the expense
    :except Exception if an error occurs communicating with the db
    """
    try:
        with Session(_engine) as session:
            stmt = select(ExpenseTbl).where(
                and_(
                    ExpenseTbl.id == expense_id,
                    ExpenseTbl.author_id == user_id
                )
            )
            result = session.scalars(stmt).all()
            return len(result) > 0
    except Exception as e:
        raise Exception(f"An error occurred retrieving a user from the db: {e}")
