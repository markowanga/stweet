"""ScrapBatchBadResponse definition."""


class ScrapBatchBadResponse(Exception):
    """ScrapBatchBadResponse class."""

    def __init__(self, msg):
        """Error constructor."""
        super().__init__(msg)
