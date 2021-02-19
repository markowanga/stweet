"""ScrapBatchBadResponse class."""


class UserSuspendedException(Exception):
    """ScrapBatchBadResponse class."""

    def __init__(self):
        """Error constructor."""
        super().__init__('Username is suspended')
