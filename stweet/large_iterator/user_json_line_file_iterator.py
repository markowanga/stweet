"""Iterator to parse Users from JSON lines."""
from .object_file_iterator import ObjectFileIterator
from ..mapper.user_json_mapper import create_user_from_json
from ..model import User


class UserJsonLineFileIterator(ObjectFileIterator[User]):
    """Iterator to parse Users from JSON lines."""

    def _parse_line(self, line: str) -> User:
        """Parse User from JSON line."""
        return create_user_from_json(line)
