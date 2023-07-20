class UsernameExistsError(Exception):
    """
    Error when a user tries to create an account with an existing username
    """
    pass

class UnauthorizedError(Exception):
    """
    Error when trying to query something that does not belong to them
    """
    pass

class DoesNotExistError(Exception):
    """
    Error when trying to query or reference something that does not exist
    """
    pass
