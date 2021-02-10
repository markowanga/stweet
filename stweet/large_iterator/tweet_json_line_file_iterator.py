"""Iterator to parse Tweet from JSON lines."""
from .object_file_iterator import ObjectFileIterator
from .. import Tweet
from ..mapper.tweet_json_mapper import create_tweet_from_json


class TweetJsonLineFileIterator(ObjectFileIterator[Tweet]):
    """Iterator to parse Tweet from JSON lines."""

    def _parse_line(self, line: str) -> Tweet:
        """Parse Tweet from JSON line."""
        return create_tweet_from_json(line)
