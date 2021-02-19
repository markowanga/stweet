"""GuestAuthException class."""


class GuestAuthException(Exception):
    """GuestAuthException class."""

    def __init__(self, request_url: str):
        """Error constructor."""
        super().__init__(f'problem with guest auth exception {request_url}')
