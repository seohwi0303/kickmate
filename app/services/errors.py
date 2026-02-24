class HandleAlreadyExists(Exception):
    """Raised when a user handle already exists."""
    pass


class UserNotFound(Exception):
    """Raised when a user is not found."""
    pass