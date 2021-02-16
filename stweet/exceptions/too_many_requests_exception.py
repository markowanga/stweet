class TooManyRequestsException(Exception):
    """ScrapBatchBadResponse class."""

    def __init__(self, request_url: str):
        """Error constructor."""
        super().__init__(f'to many requests to {request_url}')
