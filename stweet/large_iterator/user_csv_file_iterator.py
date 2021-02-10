from .object_file_iterator import ObjectFileIterator
from ..import_data import parse_user_from_csv_line
from ..model import User


class UserCsvFileIterator(ObjectFileIterator[User]):
    """Iterator to parse Users from csv lines."""

    def _parse_line(self, line: str) -> User:
        """Parse User from csv line."""
        return parse_user_from_csv_line(line)
