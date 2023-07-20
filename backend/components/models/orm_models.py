from datetime import datetime
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class AuthUserTbl(Base):
    __tablename__ = "auth_user"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))


class UserTbl(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))


ExpenseGroupMembers = Table(
    "expense_group_members",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("expense_group.id")),
    Column("user_id", Integer, ForeignKey("user.id")),
)


class ExpenseTbl(Base):
    __tablename__ = "expense"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float]
    date: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("expense_group.id"))


class ExpenseGroupTbl(Base):
    __tablename__ = "expense_group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    expenses: Mapped[List["ExpenseTbl"]] = relationship()
    users: Mapped[List["UserTbl"]] = relationship(secondary=ExpenseGroupMembers)
