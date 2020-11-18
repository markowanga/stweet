"""TokenExpiryException definition."""


class TokenExpiryException(Exception):
    """TokenExpiryException class."""

    def __init__(self, msg):
        """Error constructor."""
        super().__init__(msg)
