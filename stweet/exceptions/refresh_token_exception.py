"""RefreshTokenException definition."""


class RefreshTokenException(Exception):
    """RefreshTokenException class."""

    def __init__(self, msg):
        """Error constructor."""
        super().__init__(msg)
