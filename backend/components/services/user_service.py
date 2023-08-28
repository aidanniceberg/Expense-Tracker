from typing import List
from components.models.user import User
from components.daos import auth_dao, user_dao

def create_user(username: str, hashed_password: str, first_name: str, last_name: str, email: str) -> None:
    """
    Creates a user by adding them to the user and auth user tables
    """
    user_id = user_dao.create_user(username, first_name, last_name, email)
    auth_dao.create_user(user_id, username, hashed_password)

def get_users() -> List[User]:
    """
    Gets all users

    :return list of users
    """
    return user_dao.get_users()
    
