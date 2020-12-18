"""InvalidRequestsParamException definition."""


class InvalidRequestsParamException(Exception):
    """InvalidRequestsParamException class."""

    def __init__(self, msg):
        """Error constructor."""
        super().__init__(msg)
